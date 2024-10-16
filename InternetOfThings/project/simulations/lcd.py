import json
import random
import time
import paho.mqtt.client as mqtt


humidity = 0
temperature = 0
DHT_NAME = "GDHT"


def on_connect(client, userdata, flags, rc):
    client.subscribe("data/temperature")
    client.subscribe("data/humidity")


def update_data(topic, data):
    global humidity, temperature
    if data["name"] == DHT_NAME:
        if topic == "data/temperature":
            temperature = data["value"]
        elif topic == "data/humidity":
            humidity = data["value"]


def connect_mqtt(hostname,port):
    mqtt_client = mqtt.Client()
    mqtt_client.connect(hostname,port, 60)
    mqtt_client.loop_start()
    mqtt_client.on_connect = on_connect
    mqtt_client.on_message = lambda client, userdata, msg: update_data(msg.topic, json.loads(msg.payload.decode('utf-8')))


def run_lcd_simulator(delay, callback, stop_event, settings,hostname,port):
    connect_mqtt(hostname,port)
    while True:
        callback(humidity, temperature, settings)
        if stop_event.is_set():
            break
        time.sleep(delay)
