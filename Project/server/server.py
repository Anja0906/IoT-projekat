import threading
from queue import Queue

from flask import Flask, jsonify, request
from flask_cors import CORS
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
import paho.mqtt.client as mqtt
import json
import os
from dotenv import load_dotenv
import paho.mqtt.publish as publish

from Project.project_settings.settings import load_settings
from querry_service import query_dus_sensor

load_dotenv()

app = Flask(__name__)
CORS(app)
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
    "BedroomInfrared"
]


def handle_temperature(data):
    print(f"Obrada podataka o temperaturi: {data}")


def handle_humidity(data):
    print(f"Obrada podataka o vlažnosti: {data}")


def handle_motion(data):
    global broj_osoba_u_objektu
    if (data["name"] == "DPIR1" or data["name"] == "DPIR2"):
        dus = "DUS1" if data["name"] == "DPIR1" else "DUS2"
        is_entering = query_dus_sensor(influxdb_client, org, dus)
        if is_entering:
            broj_osoba_u_objektu += 1
        elif broj_osoba_u_objektu > 0:
            broj_osoba_u_objektu -= 1
    elif (broj_osoba_u_objektu == 0):
        mqtt_client.publish("Alarm", "Oglasio se alarm na: " + data["name"])


# Todo:Aktiviraj alarm


def handle_door_sensor(data):
    print(f"Obrada podataka sa senzora vrata: {data}")


def on_connect(client, userdata, flags, rc):
    for topic in topics:
        client.subscribe(topic)


def on_message(client, userdata, msg):
    batch_data = json.loads(msg.payload.decode('utf-8'))
    data = json.loads(msg.payload.decode('utf-8'))
    save_to_db(data)
    topic = data['measurement']
    # print(topic)
    if topic == "Motion":
        handle_motion(data)

    # mqtt_client.publish()
    # print(topic)
    # if topic and topic in topic_functions:
    #     topic_functions[topic](data)
    # else:
    #     print(f"Nepoznat ili nedostajući topic: {topic}")


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


if __name__ == '__main__':
    app.run(debug=True)
