import threading
import time
import json
from datetime import datetime

import paho.mqtt.publish as publish
from sensors.broker_settings import HOSTNAME, PORT

result = True
dioda_batch = []
publish_data_counter = 0
publish_data_limit = 5
counter_lock = threading.Lock()


def publisher_task(event, batch):
    global publish_data_counter, publish_data_limit
    while True:
        event.wait()
        with counter_lock:
            local_dioda_batch = batch.copy()
            publish_data_counter = 0
            batch.clear()
        publish.multiple(local_dioda_batch, hostname=HOSTNAME, port=PORT)
        event.clear()


publish_event = threading.Event()
publisher_thread = threading.Thread(target=publisher_task, args=(publish_event, dioda_batch))
publisher_thread.daemon = True
publisher_thread.start()


def dl_callback(publish_event, settings, code, verbose=False):
    global  publish_data_counter, publish_data_limit
    t = time.localtime()

    print("=" * 20)
    print(f"Timestamp: {time.strftime('%H:%M:%S', t)}")
    dioda_payload = {
        "measurement": "DoorLight",
        "simulated": settings['simulated'],
        "runs_on": settings["runs_on"],
        "name": settings["name"],
        "value": verbose
    }

    with counter_lock:
        dioda_batch.append(('DoorLight', json.dumps(dioda_payload), 0, True))
        publish_data_counter += 1

    if publish_data_counter >= publish_data_limit:
        publish_event.set()


def dioda_light_control(publish_event, settings, motion_detected_event, code):
    timer = None

    def turn_off_light():
        nonlocal timer
        print("Svetlo se gasi.")
        dl_callback(publish_event, settings, code, verbose=False)

    while True:
        motion_detected_event.wait()
        if timer is not None:
            timer.cancel()
        print("Svetlo se pali.")
        dl_callback(publish_event, settings, code, verbose=True)

        timer = threading.Timer(10, turn_off_light)
        timer.start()

        motion_detected_event.clear()


def run_dl(settings, threads, stop_event, code):
    if settings['simulated']:
        dl_thread = threading.Thread(target=dioda_light_control, args=(publish_event, settings, stop_event, code))
        dl_thread.start()
        threads.append(dl_thread)
    else:
        pin = settings['pin']
        from actuators.dioda import run_dl
        dms_thread = threading.Thread(target=run_dl, args=(pin, dl_callback, publish_event, settings, code))
        dms_thread.start()
        threads.append(dms_thread)
