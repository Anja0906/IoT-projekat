import json
import threading

import paho.mqtt.client as mqtt

from components.broker_settings import HOSTNAME, PORT

client = mqtt.Client()
client.connect(HOSTNAME, PORT, 60)
client.subscribe("simulator/changeRgbColor")
client.loop_start()

on_message_thread_event = threading.Event()

SimulatedButtons = [0x300ff22dd, 0x300ffc23d, 0x300ff629d, 0x300ffa857, 0x300ff9867, 0x300ffb04f, 0x300ff6897,
                    0x300ff02fd, 0x300ff30cf, 0x300ff18e7, 0x300ff7a85, 0x300ff10ef, 0x300ff38c7, 0x300ff5aa5,
                    0x300ff42bd, 0x300ff4ab5, 0x300ff52ad]
ButtonsNames = ["LEFT", "RIGHT", "UP", "DOWN", "2", "3", "1", "OK", "4", "5", "6", "7", "8", "9", "*", "0",
                "#"]

current_button_name = "0"
current_button_hex = 0x300ff4ab5


def get_current_button_name():
    return current_button_name


def get_button_name(button_hex):
    index = SimulatedButtons.index(button_hex)
    button_name = ButtonsNames[index] if index < len(ButtonsNames) else "Unknown"
    return button_name


def on_message(client, userdata, message):
    data = json.loads(message.payload.decode())
    hex_value = data.get('hex_value')
    if hex_value is not None:
        int_value = int(hex_value, 16)
        set_current_hex(int_value)
    else:
        print("Hex value not found in the message")


client.on_message = on_message


def set_current_hex(button_hex):
    global current_button_name, current_button_hex
    current_button_hex = button_hex
    current_button_name = get_button_name(button_hex)
    client.publish("RGBSet", current_button_name)
    on_message_thread_event.set()


def run_simulation(delay, callback, stop_event, publish_event, settings, code):
    while True:
        on_message_thread_event.wait()
        callback(get_current_button_name(), publish_event, settings, code)
        on_message_thread_event.clear()
