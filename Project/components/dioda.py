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
    global result, publish_data_counter, publish_data_limit
    t = time.localtime()
    print("=" * 20)
    print(f"Timestamp: {time.strftime('%H:%M:%S', t)}")
    if result:
        result = False
        print("Light is on\n")
    else:
        result = True
        print("Light is off\n")
    dioda_payload = {
        "measurement": "DoorLight",
        "simulated": settings['simulated'],
        "runs_on": settings["runs_on"],
        "name": settings["name"],
        "value": result
    }

    with counter_lock:
        dioda_batch.append(('DoorLight', json.dumps(dioda_payload), 0, True))
        publish_data_counter += 1

    if publish_data_counter >= publish_data_limit:
        publish_event.set()


def run_dl(settings, threads, stop_event, code):
    if settings['simulated']:
        dl_thread = threading.Thread(target=dl_callback, args=(publish_event, settings, code))
        dl_thread.start()
        threads.append(dl_thread)
    else:
        pin = settings['pin']
        from actuators.dioda import run_dl
        dms_thread = threading.Thread(target=run_dl, args=(pin, code))
        dms_thread.start()
        threads.append(dms_thread)

