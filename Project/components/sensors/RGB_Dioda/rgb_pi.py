import json
import threading

import RPi.GPIO as GPIO
from time import sleep
import paho.mqtt.client as mqtt

from components.broker_settings import HOSTNAME, PORT
client = mqtt.Client()
client.connect(HOSTNAME, PORT, 60)
client.subscribe("RGBSet")
client.loop_start()
color = '0'
# disable warnings (optional)
GPIO.setwarnings(False)
set_new_color_event = threading.Event()
GPIO.setmode(GPIO.BCM)

RED_PIN = 12
GREEN_PIN = 13
BLUE_PIN = 19

# set pins as outputs
GPIO.setup(RED_PIN, GPIO.OUT)
GPIO.setup(GREEN_PIN, GPIO.OUT)
GPIO.setup(BLUE_PIN, GPIO.OUT)

def on_message(client, userdata, message):
    color = json.loads(message.payload.decode())

client.on_message = on_message

def turnOff(callback, stop_event, publish_event, settings, code):
    GPIO.output(RED_PIN, GPIO.LOW)
    GPIO.output(GREEN_PIN, GPIO.LOW)
    GPIO.output(BLUE_PIN, GPIO.LOW)
    callback("Off", publish_event, settings, code)


def white(callback, stop_event, publish_event, settings, code):
    GPIO.output(RED_PIN, GPIO.HIGH)
    GPIO.output(GREEN_PIN, GPIO.HIGH)
    GPIO.output(BLUE_PIN, GPIO.HIGH)
    callback("White", publish_event, settings, code)


def red(callback, stop_event, publish_event, settings, code):
    GPIO.output(RED_PIN, GPIO.HIGH)
    GPIO.output(GREEN_PIN, GPIO.LOW)
    GPIO.output(BLUE_PIN, GPIO.LOW)
    callback("Red", publish_event, settings, code)


def green(callback, stop_event, publish_event, settings, code):
    GPIO.output(RED_PIN, GPIO.LOW)
    GPIO.output(GREEN_PIN, GPIO.HIGH)
    GPIO.output(BLUE_PIN, GPIO.LOW)
    callback("Green", publish_event, settings, code)


def blue(callback, stop_event, publish_event, settings, code):
    GPIO.output(RED_PIN, GPIO.LOW)
    GPIO.output(GREEN_PIN, GPIO.LOW)
    GPIO.output(BLUE_PIN, GPIO.HIGH)
    callback("Blue", publish_event, settings, code)


def yellow(callback, stop_event, publish_event, settings, code):
    GPIO.output(RED_PIN, GPIO.HIGH)
    GPIO.output(GREEN_PIN, GPIO.HIGH)
    GPIO.output(BLUE_PIN, GPIO.LOW)
    callback("Yellow", publish_event, settings, code)


def purple(callback, stop_event, publish_event, settings, code):
    GPIO.output(RED_PIN, GPIO.HIGH)
    GPIO.output(GREEN_PIN, GPIO.LOW)
    GPIO.output(BLUE_PIN, GPIO.HIGH)
    callback("Purple", publish_event, settings, code)


def lightBlue(callback, stop_event, publish_event, settings, code):
    GPIO.output(RED_PIN, GPIO.LOW)
    GPIO.output(GREEN_PIN, GPIO.HIGH)
    GPIO.output(BLUE_PIN, GPIO.HIGH)
    callback("Light Blue", publish_event, settings, code)


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


def run_rgb_dioda(delay, callback, stop_event, publish_event, settings, code):
    try:
        while True:
            set_new_color_event.wait()
            if color == "*":
                turnOff(callback, stop_event, publish_event, settings, code)
            elif color == "1":
                red(callback, stop_event, publish_event, settings, code)
            elif color == "2":
                green(callback, stop_event, publish_event, settings, code)
            elif color == "3":
                blue(callback, stop_event, publish_event, settings, code)
            elif color == "4":
                yellow(callback, stop_event, publish_event, settings, code)
            elif color == "5":
                purple(callback, stop_event, publish_event, settings, code)
            elif color == "6":
                lightBlue(callback, stop_event, publish_event, settings, code)
            elif color == "7":
                white(callback, stop_event, publish_event, settings, code)
            set_new_color_event.clear()
    except KeyboardInterrupt:
        GPIO.cleanup()
    except Exception as e:
        print(f'Error: {str(e)}')
