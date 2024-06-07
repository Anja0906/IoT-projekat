import json
import random
import time
import paho.mqtt.client as mqtt

status = "off"
new_action = "off"
all_states = ["red", "green", "blue", "yellow", "purple", "lightBlue", "white", "off"]

def map_color(key):
    if key == "1":
        return "red"
    elif key == "2":
        return "green"
    elif key == "3":
        return "blue"
    elif key == "4":
        return "yellow"
    elif key == "5":
        return "lightBlue"
    elif key == "6":
        return "purple"
    elif key == "0":
        return "off"
    else:
        return "white"


def on_connect(client, userdata, flags, rc):
    client.subscribe("data/ir")
    client.subscribe("change/rgb")

def update_data(topic, data):
    global new_action
    print("rgb data: ", data, "received from topic " + topic)
    new_action = map_color(data["value"])

def connect_mqtt():
    mqtt_client = mqtt.Client()
    mqtt_client.connect("localhost", 1883, 60)
    mqtt_client.loop_start()
    mqtt_client.on_connect = on_connect
    mqtt_client.on_message = lambda client, userdata, msg: update_data(msg.topic, json.loads(msg.payload.decode('utf-8')))


def run_rgb_simulator(delay, callback, stop_event, publish_event, settings):
    connect_mqtt()
    global status, new_action
    while True:
        if new_action != status:
            status = new_action
            callback(status, publish_event, settings)
        if stop_event.is_set():
            break
        time.sleep(delay)
