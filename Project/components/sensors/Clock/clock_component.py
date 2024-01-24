import threading
import json
from datetime import datetime

import paho.mqtt.publish as publish
from components.broker_settings import HOSTNAME, PORT
from components.sensors.Clock.clock_simulation import run_display_simulator

clock_batch = []
publish_data_counter = 0
publish_data_limit = 5
counter_lock = threading.Lock()


def display_callback(time, publish_event, settings, code):
    global publish_data_counter, publish_data_limit
    print("Vreme je: " + time)
    clock_payload = {
        "measurement": "Clock",
        "simulated": settings['simulated'],
        "runs_on": settings["runs_on"],
        "name": settings["name"],
        "value": time
    }
    with counter_lock:
        clock_batch.append(('Clock', json.dumps(clock_payload), 0, True))
        publish_data_counter += 1

    if publish_data_counter >= publish_data_limit:
        publish_event.set()


def publisher_task(event, batch):
    global publish_data_counter, publish_data_limit
    while True:
        event.wait()
        with counter_lock:
            local_clock_batch = batch.copy()
            publish_data_counter = 0
            batch.clear()
        publish.multiple(local_clock_batch, hostname=HOSTNAME, port=PORT)
        event.clear()


publish_event = threading.Event()
publisher_thread = threading.Thread(target=publisher_task, args=(publish_event, clock_batch))
publisher_thread.daemon = True
publisher_thread.start()


def run_clock(settings, threads, alarm_event, code):
    if settings['simulated']:
        print("Starting " + code + " simulator")
        clock_thread = threading.Thread(target=run_display_simulator,
                                      args=(1, display_callback, alarm_event, publish_event, settings, code))
        clock_thread.start()
        threads.append(clock_thread)
        print(code + " simulator started\n")
    else:
        from clock_pi import run_clock
        print("Starting " + code + " loop")
        dms_thread = threading.Thread(target=run_clock,
                                      args=(2, display_callback, alarm_event, publish_event, settings, code))
        dms_thread.start()
        threads.append(dms_thread)
        print(code + " loop started")
