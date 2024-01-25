import json
import threading
import time
import random

from components.broker_settings import HOSTNAME, PORT

ir_changed_event1 = threading.Event()
from components.sensors.IR.ir_simulation import get_current_button_name
import paho.mqtt.client as mqtt
mqtt_client = mqtt.Client()
mqtt_client.connect(HOSTNAME, PORT, 60)
mqtt_client.loop_start()
mqtt_client.subscribe("RGBChanged")
from project_settings.settings import load_settings
ButtonsNames = ["LEFT", "RIGHT", "UP", "DOWN", "2", "3", "1", "OK", "4", "5", "6", "7", "8", "9", "*", "0",
                "#"]
def print_color(value):
    colors = {
        "0": "Off",
        "1": "White",
        "2": "Red",
        "3": "Green",
        "4": "Blue",
        "5": "Yellow",
        "6": "Purple",
        "7": "Light Blue"
    }
    return colors.get(value, "Unknown")

def on_message(client, userdata, msg):
    ir_changed_event1.set()

mqtt_client.on_message = on_message


def run_rgb_dioda_simulation(delay, callback, ir_changed_event, publish_event, settings, code):
    while True:
        ir_changed_event1.wait()
        color = print_color(get_current_button_name())
        print(color)
        if color != "Unknown":
            callback(color, publish_event, settings, code)
        time.sleep(delay)
        ir_changed_event1.clear()