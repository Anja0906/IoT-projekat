import threading
import time
import os
from dotenv import load_dotenv
from flask_socketio import SocketIO
from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
import paho.mqtt.client as mqtt
import json
from settings import load_settings
from datetime import datetime, timedelta

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="http://localhost:3001", async_mode='threading')

# InfluxDB Configuration
token = os.getenv("INFLUXDB_TOKEN")
org = os.getenv("ORGANIZATION")
url = os.getenv("URL")
bucket = os.getenv("BUCKET_NAME")
influxdb_client = InfluxDBClient(url=url, token=token, org=org)

mqtt_client = mqtt.Client()
mqtt_client.connect("localhost", 1883, 0)
mqtt_client.loop_start()
in_house_count = 0
is_alarm = False
house_keep = False
lock = threading.Lock()
last_pressed_ds1 = 0
last_released_ds1 = 0
last_pressed_ds2 = 0
last_released_ds2 = 0
correct_pin = "1234"
security_timestamp = time.time()
last_correct_pin = 0

bb_alarm_time = "21:39"

def alarm_set_on():
    print("ALARM")
    with app.app_context():
        with lock:
            global is_alarm
            is_alarm = True
            mqtt_client.publish("pi1", json.dumps({"trigger": "B"}))
            mqtt_client.publish("pi3", json.dumps({"trigger": "B"}))
            point = (
                Point("Alarm")
                .tag("name", "triggered")
                .field("Is_alarm", "on" if is_alarm else "off")
            )
        write_api = influxdb_client.write_api(write_options=SYNCHRONOUS)
        write_api.write(bucket=bucket, org=org, record=point)
        send_alarm_to_client()

def alarm_set_off():
    with app.app_context():
        with lock:
            global is_alarm
            is_alarm = False
            mqtt_client.publish("pi1", json.dumps({"trigger": "D"}))
            mqtt_client.publish("pi3", json.dumps({"trigger": "D"}))
            point = (
                Point("Alarm")
                .tag("name", "triggered")
                .field("Is_alarm", "on" if is_alarm else "off")
            )
        write_api = influxdb_client.write_api(write_options=SYNCHRONOUS)
        write_api.write(bucket=bucket, org=org, record=point)
        send_alarm_to_client()

@socketio.on('connect')
def handle_connect():
    print('Client connected successfully\n')

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected successfully\n')

def send_data_to_client(data):
    try:
        socketio.emit('data', {'message': data})
    except Exception as e:
        print(e)

def send_alarm_to_client():
    global is_alarm
    try:
        socketio.emit('alarm', {'message': is_alarm})
    except Exception as e:
        print(e)

def on_connect(client, userdata, flags, rc):
    print("Connected to MQTT broker with result code " + str(rc))
    client.subscribe("data/+")

mqtt_client.on_connect = on_connect
mqtt_client.on_message = lambda client, userdata, msg: save_to_db(msg.topic, json.loads(msg.payload.decode('utf-8')))

def laj_koji_pase_ne_ujeda():
    global last_pressed_ds1
    global last_pressed_ds2
    global security_timestamp
    global house_keep
    while True:
        if house_keep:
            if last_pressed_ds1 > 0 and time.time() - last_pressed_ds1 > 5 and last_released_ds1 <= last_pressed_ds1:
                alarm_set_on()
            if last_pressed_ds2 > 0 and time.time() - last_pressed_ds2 > 5 and last_released_ds2 <= last_pressed_ds2:
                alarm_set_on()
            if security_timestamp > time.time():
                if (last_released_ds2 > last_pressed_ds2 and
                        time.time() - max(last_pressed_ds2, last_released_ds2) > 5 and time.time() - last_correct_pin > 5):
                    alarm_set_on()
                if (last_released_ds1 > last_pressed_ds1 and
                        time.time() - max(last_pressed_ds1, last_released_ds1) > 5 and time.time() - last_correct_pin > 5):
                    alarm_set_on()
        time.sleep(1)

def adjust_people_count(device_number=1):
    with app.app_context():
        query = (f'from(bucket: "{bucket}") |> range(start: -5s, stop: now()) |> filter(fn: ('
                 f'r) => r["_measurement"] == "UDS") |> filter(fn: (r) => r["name"] == "DUS{device_number}") '
                 f' |> yield(name: "last")')
        response = handle_influx_query(query)

        try:
            values = json.loads(response.data.decode('utf-8'))['data']
        except KeyError:
            print("Key 'data' not found in the response")
            return

        values_list = [item["_value"] for item in values]
        gain = sum([j - i for i, j in zip(values_list[:-1], values_list[1:])])

        with lock:
            global in_house_count
            if len(values) > 0:
                if gain > 0:
                    in_house_count += 1
                elif gain < 0:
                    in_house_count -= 1
                if in_house_count < 0:
                    in_house_count = 0

            point = (
                Point("People_count")
                .tag("name", "overall")
                .field("population", in_house_count)
            )
        write_api = influxdb_client.write_api(write_options=SYNCHRONOUS)
        write_api.write(bucket=bucket, org=org, record=point)

def integrate(values, delta_t):
    integral = 0
    for i in range(1, len(values)):
        integral += (values[i] + values[i-1]) / 2 * delta_t
    return integral

def check_safe_movement(data):
    with app.app_context():
        axis = str(data["axis"])

        query = (f'from(bucket: "{bucket}") |> range(start: -10s, stop: now())'
                 '|> filter(fn: (r) => r["_measurement"] == "Gyroscope")'
                 '|> filter(fn: (r) => r["name"] == "GSG")'
                 f'|> filter(fn: (r) => r["axis"] == "{axis}")'
                 '|> aggregateWindow(every: 5s, fn: last, createEmpty: false)'
                 '|> yield(name: "last")')
        response = handle_influx_query(query)
        values = json.loads(response.data.decode('utf-8'))['data']

        global is_alarm
        global house_keep

        if len(values) > 1 and house_keep:
            time_format = '%a, %d %b %Y %H:%M:%S %Z'
            t1 = datetime.strptime(values[0]["_time"], time_format)
            t2 = datetime.strptime(values[1]["_time"], time_format)
            delta_t = (t2 - t1).total_seconds()
            gyro_values = [v["_value"] for v in values]
            displacement = integrate(gyro_values, delta_t)
            threshold = 10  
            if abs(displacement) > threshold:
                print("DEGAS")
                alarm_set_on()
                
                
def rpir_raise_alarm():
    with app.app_context():
        global is_alarm
        global in_house_count
        global house_keep
        if in_house_count == 0 and house_keep:
            alarm_set_on()

def ds_adjust_time(data, device_number=1):
    if data["value"] == "pressed":
        if device_number == 1:
            with lock:
                global last_pressed_ds1
                last_pressed_ds1 = time.time()
        else:
            with lock:
                global last_pressed_ds2
                last_pressed_ds2 = time.time()
    else:
        if device_number == 1:
            with lock:
                global last_released_ds1
                last_released_ds1 = time.time()
        else:
            with lock:
                global last_released_ds2
                last_released_ds2 = time.time()

def handle_pin_input(pin):
    with app.app_context():
        if pin == correct_pin:
            global is_alarm
            global security_timestamp
            if is_alarm:
                alarm_set_off()
            if security_timestamp == 0:
                with lock:
                    security_timestamp = time.time() + 10
            else:
                with lock:
                    security_timestamp = 0

            with lock:
                global last_correct_pin
                last_correct_pin = time.time()
                point = (
                    Point("Alarm")
                    .tag("name", "active")
                    .field("Is_alarm", "on" if security_timestamp > 0 else "off")
                )
            write_api = influxdb_client.write_api(write_options=SYNCHRONOUS)
            write_api.write(bucket=bucket, org=org, record=point)

def command_callback(data):
    if data["name"] == "DPIR1" and data['value'] == "detected":
        mqtt_client.publish("pi1", json.dumps({"trigger": "L"}))
        adjust_people_count()
    if data["name"] == "DPIR2" and data['value'] == "detected":
        adjust_people_count(2)
    if data["name"] == "GSG":
        check_safe_movement(data)
    if data['value'] == "detected" and (
            data["name"] == "RPIR1" or data["name"] == "RPIR2" or data["name"] == "RPIR3" or data["name"] == "RPIR4"):
        rpir_raise_alarm()
    if data["name"] == "DS1":
        ds_adjust_time(data)
    if data["name"] == "DS2":
        ds_adjust_time(data, 2)
    if data["name"] == "DMS":
        handle_pin_input(data["value"])



def save_to_db(topic, data):
    write_api = influxdb_client.write_api(write_options=SYNCHRONOUS)
    if isinstance(data["value"], int):
        data["value"] = float(data["value"])

    if topic == "data/acceleration" or topic == "data/gyroscope":
        point = (
            Point(data["measurement"])
            .tag("simulated", data["simulated"])
            .tag("runs_on", data["runs_on"])
            .tag("name", data["name"])
            .tag("axis", data.get("axis", ""))  
            .field("value", data["value"])  
        )
    else:
        point = (
            Point(data["measurement"])
            .tag("simulated", data["simulated"])
            .tag("runs_on", data["runs_on"])
            .tag("name", data["name"])
            .field("value", data["value"])  
        )
    if data["name"] == "BRGB":  
        print(data)

    write_api.write(bucket=bucket, org=org, record=point)
    command_callback(data)
    send_data_to_client(data)  
    try:
        if data.get("is_last"): 
            send_data_to_client(data)
    except Exception as e:
        print(e)

def handle_influx_query(query):
    try:
        query_api = influxdb_client.query_api()
        tables = query_api.query(query, org=org)

        container = []
        for table in tables:
            for record in table.records:
                container.append(record.values)

        return jsonify({"status": "success", "data": container})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

def extract_filtered_device_info():
    settings = load_settings()
    filtered_info = {
        key: {
            "name": device_info["name"],
            "simulated": device_info["simulated"],
            "pin": device_info.get("pin", None),
            "runs_on": device_info["runs_on"]
        }
        for key, device_info in settings.items()
    }
    return filtered_info

@app.route('/api/device_info', methods=['GET'])
@cross_origin()
def retrieve_filtered_device_info():
    filtered_device_info = extract_filtered_device_info()
    print(filtered_device_info)
    return jsonify(filtered_device_info)

@app.route('/api/active', methods=['GET'])
@cross_origin()
def active_system():
    global house_keep
    house_keep = True
    print("System activated")
    return jsonify({"status": "success", "message": "System activated"})

@app.route('/api/deactive', methods=['GET'])
@cross_origin()
def deactive_system():
    global house_keep
    house_keep = False
    print("System deactivated")
    return jsonify({"status": "success", "message": "System deactivated"})

@app.route('/api/device_values', methods=['GET'])
@cross_origin()
def retrieve_device_values():
    query = f'from(bucket: "{bucket}") |> range(start: -5m) |> filter(fn: (r) => r["_measurement"] != "Alarm") |> last()'
    response = handle_influx_query(query)
    values = json.loads(response.data.decode('utf-8'))['data']
    device_values = {}

    for value in values:
        device_name = value["name"]
        device_values[device_name] = {
            "value": value["_value"],
            "measurement": value["_measurement"],
            "time": value["_time"]
        }
        print(device_values[device_name])

    return jsonify({"status": "success", "data": device_values})

@app.route('/api/updateRGB/<color>', methods=['GET'])
@cross_origin()
def update_rgb(color):
    print(color)
    rgb_topic = "front-rgb"
    payload = json.dumps({"value": color})
    mqtt_client.publish(rgb_topic, payload)
    return payload

@app.route('/api/getAlarmClock', methods=['GET'])
@cross_origin()
def get_alarm_clock():
    print("api to get alarm clock")
    payload = json.dumps({"time": bb_alarm_time})
    return payload

@app.route('/api/setAlarmClock', methods=['PUT'])
@cross_origin()
def set_alarm_clock():
    global bb_alarm_time
    try:
        data = request.json
        bb_alarm_time = data.get('time').strip()  # Trimovanje eventualnih belih znakova

        # Validate and sanitize time format
        try:
            # Debug: print the time value
            print(f"Received time: '{bb_alarm_time}'")
            datetime.strptime(bb_alarm_time, "%H:%M")
        except ValueError as e:
            print(f"Time format error: {e}")
            return jsonify({'error': 'Invalid time format. Use HH:MM'}), 400

        print("Alarm clock time changed to ", bb_alarm_time)
        bb_topic = "front-bb-on"
        payload = json.dumps({"time": bb_alarm_time})
        mqtt_client.publish(bb_topic, payload)
        return jsonify({'message': 'Alarm time set successfully'})
    except Exception as e:
        print(f"Exception occurred: {e}")
        return jsonify({'error': str(e)}), 500


    
    
@app.route('/api/inputPin', methods=['PUT'])
@cross_origin()
def input_pin():
    try:
        data = request.json
        pin = data.get('pin')
        print("Pin entered: ", pin)
        handle_pin_input(pin)
        return jsonify({'message': 'Pin entered successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/turnOffAlarmClock', methods=['GET'])
@cross_origin()
def turn_off_alarm_clock():
    try:
        print("turn off alarm clock")
        bb_topic = "front-bb-off"
        payload = json.dumps({"time": ""})
        mqtt_client.publish(bb_topic, payload)
        return jsonify({'message': 'Alarm time turned off successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    laj = threading.Thread(target=laj_koji_pase_ne_ujeda)
    laj.daemon = True
    laj.start()

    app.run(debug=False, port=8000)