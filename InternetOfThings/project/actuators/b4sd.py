import time

import RPi.GPIO as GPIO
import paho.mqtt.client as mqtt

delay = 0.001

def on_connect(client, userdata, flags, rc):
    client.subscribe("front-bb-on")
    client.subscribe("front-bb-off")

def update_data(topic, data):
    global delay
    print("bb data: ", data, "received from topic " + topic)
    if topic == "front-bb-on":
        delay = 0.5
    elif topic == "front-bb-off":
        delay = 0.001

def connect_mqtt(hostname,port):
    mqtt_client = mqtt.Client()
    mqtt_client.connect(hostname, port, 60)
    mqtt_client.loop_start()
    mqtt_client.on_connect = on_connect
    mqtt_client.on_message = lambda client, userdata, msg: update_data(msg.topic, json.loads(msg.payload.decode('utf-8')))


class B4SD:
    def __init__(self, settings):
        # GPIO ports for the 7seg pins
        self.segments = settings["segments"]
        for segment in self.segments:
            GPIO.setup(segment, GPIO.OUT)
            GPIO.output(segment, 0)

        self.digits = settings["digits"]
        for digit in self.digits:
            GPIO.setup(digit, GPIO.OUT)
            GPIO.output(digit, 1)

        self.name = settings["name"]
        self.num = {' ': (0, 0, 0, 0, 0, 0, 0),
               '0': (1, 1, 1, 1, 1, 1, 0),
               '1': (0, 1, 1, 0, 0, 0, 0),
               '2': (1, 1, 0, 1, 1, 0, 1),
               '3': (1, 1, 1, 1, 0, 0, 1),
               '4': (0, 1, 1, 0, 0, 1, 1),
               '5': (1, 0, 1, 1, 0, 1, 1),
               '6': (1, 0, 1, 1, 1, 1, 1),
               '7': (1, 1, 1, 0, 0, 0, 0),
               '8': (1, 1, 1, 1, 1, 1, 1),
               '9': (1, 1, 1, 1, 0, 1, 1)}

    def show_value(self):
        n = time.ctime()[11:13] + time.ctime()[14:16]
        s = str(n).rjust(4)
        for digit in range(4):
            for loop in range(0, 7):
                GPIO.output(self.segments[loop], self.num[s[digit]][loop])
                if (int(time.ctime()[18:19]) % 2 == 0) and (digit == 1):
                    GPIO.output(25, 1)
                else:
                    GPIO.output(25, 0)
            GPIO.output(self.digits[digit], 0)
            time.sleep(delay)
            GPIO.output(self.digits[digit], 1)
        return "{}:{}".format(n[0:2], n[2:])


def run_b4sd_loop(b4sd, delay, callback, stop_event, publish_event, settings,hostname,port):
    connect_mqtt(hostname,port)
    while True:
        value = b4sd.show_value()
        callback(value, publish_event, settings)
        if stop_event.is_set():
            GPIO.cleanup()
            break
