import threading
import time

import paho.mqtt.client as mqtt

from components.broker_settings import HOSTNAME, PORT
changed_code = threading.Event()
mqtt_client = mqtt.Client()
mqtt_client.connect(HOSTNAME, PORT, 60)
mqtt_client.loop_start()
mqtt_client.subscribe("CodeChanged")

dms_code = ""
def on_message(client, userdata, message):
    global dms_code
    dms_code = message.payload.decode()
    if len(dms_code) == 4:
        changed_code.set()

mqtt_client.on_message = on_message
def run_keypad_simulator(delay, callback, set_is_alarm_active_event, code, publish_event, settings):
    global dms_code
    while True:
        changed_code.wait()
        if settings["simulated"]:
            print(dms_code)
            time.sleep(10)
            set_is_alarm_active_event.set()
            callback(dms_code, set_is_alarm_active_event, publish_event, settings, code)
        changed_code.clear()

