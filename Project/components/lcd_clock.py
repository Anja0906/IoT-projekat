import threading
import json
import time
from datetime import datetime

import paho.mqtt.publish as publish
from sensors.broker_settings import HOSTNAME, PORT
from sensors.s_simulators.lcd_clock import run_display_simulator

clock_batch = []
publish_data_counter = 0
publish_data_limit = 5
counter_lock = threading.Lock()


def display_callback(delay, publish_event, settings, code):
    global publish_data_counter, publish_data_limit
    while True:
        load = datetime.now().strftime("%H:%M:%S")
        clock_payload = {
            "measurement": "Clock",
            "simulated": settings['simulated'],
            "runs_on": settings["runs_on"],
            "name": settings["name"],
            "value": load
        }
        with counter_lock:
            clock_batch.append(('Clock', json.dumps(clock_payload), 0, True))
            publish_data_counter += 1

        if publish_data_counter >= publish_data_limit:
            publish_event.set()
        print(load+ " MRNJAAAAU")
        time.sleep(delay)


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


def run_clock(settings, threads, stop_event, code):
    if settings['simulated']:
        print("Starting " + code + " simulator")
        lcd_thread = threading.Thread(target=display_callback,
                                      args=(10, publish_event, settings, code))
        lcd_thread.start()
        threads.append(lcd_thread)
        print(code + " simulator started\n")
    else:
        from sensors.s_components.lcd_clock import run_clock
        print("Starting " + code + " loop")
        dms_thread = threading.Thread(target=run_clock,
                                      args=(2, display_callback, stop_event, publish_event, settings, code))
        dms_thread.start()
        threads.append(dms_thread)
        print(code + " loop started")
