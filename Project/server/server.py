import datetime
import threading
from queue import Queue

import sock as sock
from flask import Flask, jsonify, request
from flask_cors import CORS
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
import paho.mqtt.client as mqtt
from flask_socketio import SocketIO

import json
import os
from dotenv import load_dotenv
import paho.mqtt.publish as publish

from project_settings.settings import load_settings
from querry_service import query_dus_sensor, query_ds_sensor, query_gyro_sensor

load_dotenv()

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app)
broj_osoba_u_objektu = 0

influxdb_token = os.environ.get('INFLUXDB_TOKEN')
org = os.environ.get('ORGANIZATION')
url = os.environ.get('URL')
bucket = os.environ.get('BUCKET_NAME')
influxdb_client = InfluxDBClient(url=url, token=influxdb_token, org=org)

mqtt_client = mqtt.Client()
mqtt_client.connect("localhost", 1883, 60)
mqtt_client.loop_start()

topics = [
    "Temperature",
    "Humidity",
    "Motion",
    "DoorSensor",
    "DoorUltraSonic",
    "MembraneSwitch",
    "Buzzer",
    "DoorLight",
    "Gyro",
    "LCD",
    "Clock",
    "RGB",
    "BedroomInfrared",
    "budilnik/on",
    "AlarmEventSet",
    "AlarmEventClear"
]


def handle_gyro(data):
    result = query_gyro_sensor(influxdb_client, org)
    print("Result: ", result)
    if result:
        mqtt_client.publish("alarm", "Oglasio se alarm na: " + data["name"])
    else:
        print("Nema alarma na gyro komponenti")


def handle_motion(data):
    global broj_osoba_u_objektu
    if data["name"] == "DPIR1" or data["name"] == "DPIR2":
        dus = "DUS1" if data["name"] == "DPIR1" else "DUS2"
        is_entering = query_dus_sensor(influxdb_client, org, dus)
        if is_entering:
            broj_osoba_u_objektu += 1
        elif broj_osoba_u_objektu > 0:
            broj_osoba_u_objektu -= 1
    elif broj_osoba_u_objektu == 0:
        mqtt_client.publish("alarm", "Oglasio se alarm na: " + data["name"])


def handle_door_sensor(data):
    ds_name = data["name"]
    result = query_ds_sensor(influxdb_client, org, ds_name)
    print("Result: ", result)
    if result:
        mqtt_client.publish("alarm", "Oglasio se alarm na: " + data["name"])
    else:
        print("Nema alarma na: " + ds_name)


def handle_changed_color(data):
    mqtt_client.publish("RGBChanged", data['value'])


def handle_budilnik_socket(data):
    print(data)
    socketio.emit('budilnik_data', data)

def handle_alarm_socket(data):
    print(data)
    socketio.emit('alarm_data', data["value"])


def on_connect(client, userdata, flags, rc):
    for topic in topics:
        client.subscribe(topic)


def on_message(client, userdata, msg):
    # global broj_osoba_u_objektu
    # print(broj_osoba_u_objektu)
    if msg.topic != "budilnik/on":
        data = json.loads(msg.payload.decode('utf-8'))
        topic = data['measurement']
        save_to_db(data)
        if topic == "Motion":
            handle_motion(data)
        elif topic == "DoorSensor":
            handle_door_sensor(data)
        elif topic == "Gyro":
            handle_gyro(data)
        elif topic == "BedroomInfrared":
            handle_changed_color(data)
        elif topic == "AlarmEventSet":
            handle_alarm_socket(data)
    else:
        handle_budilnik_socket(msg.payload.decode())



mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message


def get_server_values():
    return influxdb_client, org


def extract_keys_from_settings():
    settings = load_settings()
    return list(settings.keys())


def extract_runs_on_from_settings():
    settings = load_settings()
    unique_runs_on = {settings[key]['runs_on'] for key in settings}
    return list(unique_runs_on)


def save_to_db(data):
    write_api = influxdb_client.write_api(write_options=SYNCHRONOUS)
    point = (
        Point(data["measurement"])
            .tag("simulated", data["simulated"])
            .tag("runs_on", data["runs_on"])
            .tag("name", data["name"])
            .field("measurement", data["value"])
    )
    write_api.write(bucket=bucket, org=org, record=point)


@app.route('/store_data', methods=['POST'])
def store_data():
    try:
        data = request.get_json()
        store_data(data)
        return jsonify({"status": "success"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})


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


@app.route('/set_clock_timer', methods=['POST'])
def set_clock_timer():
    data = request.get_json()  # Pretpostavlja se da se podaci šalju kao JSON
    alarm_time = data.get('time')
    if not alarm_time:
        return jsonify({"error": "Vreme nije poslato"}), 400
    try:

        mqtt_client.publish("clock", str(alarm_time))
        return jsonify({"status": "uspešno", "time": alarm_time}), 200
    except ValueError:
        return jsonify({"error": "Neispravan format vremena"}), 400


@app.route('/delete_clock_timer', methods=['POST'])
def delete_clock_timer():
    try:
        mqtt_client.publish("clock_turn_off", "Gasenje alarma")
        return jsonify({"status": "uspešno ugaseno", "time": datetime.datetime.now()}), 200
    except ValueError:
        return jsonify({"error": "Nije ugaseno"}), 400


@app.route('/device_names', methods=['GET'])
def retrieve_device_names():
    device_names = extract_keys_from_settings()
    return jsonify(device_names)


@app.route('/simulate_alarm', methods=['GET'])
def simulate_alarm():
    message = "Alarm aktiviran"
    mqtt_client.publish("alarm", message)
    print(f"Poslata poruka: {message}")
    return jsonify({"ok": str("Ok")}), 200


@app.route('/simulate_ds1', methods=['GET'])
def simulate_ds1():
    message = "DS1 pressed"
    mqtt_client.publish("ds1", message)
    print(f"Poslata poruka: {message}")
    return jsonify({"ok": str("Ok")}), 200


@app.route('/simulate_ds2', methods=['GET'])
def simulate_ds2():
    message = "DS2 pressed"
    mqtt_client.publish("ds2", message)
    print(f"Poslata poruka: {message}")
    return jsonify({"ok": str("Ok")}), 200


@app.route('/ir_remote/<path:hex_value>', methods=['PUT'])
def process_hex(hex_value):
    try:
        int_value = int(hex_value, 16)
        mqtt_message = json.dumps({"hex_value": hex_value})
        mqtt_client.publish("simulator/changeRgbColor", mqtt_message)

        return jsonify({"message": "Hexadecimal string received", "value": hex_value}), 200
    except ValueError:
        return jsonify({"error": "Invalid hexadecimal value"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/pi_names', methods=['GET'])
def retrieve_pi_names():
    return extract_runs_on_from_settings()


@app.route('/topic_names', methods=['GET'])
def retrieve_topic_names():
    return topics


@app.route('/component_data/<name>', methods=['GET'])
def retrieve_component_data(name):
    query = f"""from(bucket: "{bucket}")
    |> range(start: -10m)
    |> filter(fn: (r) => r.name == "{name}")"""
    return handle_influx_query(query)


@app.route('/topic_data/<name>', methods=['GET'])
def retrieve_topic_data(name):
    query = f"""from(bucket: "{bucket}")
    |> range(start: -10m)
    |> filter(fn: (r) => r._measurement == "{name}")"""
    return handle_influx_query(query)


@app.route('/pi_data/<name>', methods=['GET'])
def retrieve_pi_data(name):
    query = f"""from(bucket: "{bucket}")
    |> range(start: -10m)
    |> filter(fn: (r) => r.runs_on == "{name}")"""
    return handle_influx_query(query)


@app.route('/set_code', methods=['POST'])
def handle_post():
    data = request.get_json()
    my_param = data.get('code')
    if not my_param:
        return jsonify({"error": "Parametar 'code' je obavezan"}), 400
    mqtt_client.publish("CodeChanged", my_param)
    return jsonify({"message": f"Primljeni parametar: {my_param}"}), 200


@app.route('/set_off_alarm', methods=['GET'])
def turn_off_alarm():
    mqtt_client.publish("alarm/off", "")
    return jsonify({"message": f"Alarm ugasen"}), 200

if __name__ == '__main__':
    app.run(debug=True)
