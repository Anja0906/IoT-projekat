import threading
import time
import json
from datetime import datetime

import paho.mqtt.publish as publish
from sensors.broker_settings import HOSTNAME, PORT
from actuators.buzzer import buzz

buzzer_batch = []
publish_data_counter = 0
publish_data_limit = 5
counter_lock = threading.Lock()

def publisher_task(event, batch):
    global publish_data_counter, publish_data_limit
    while True:
        event.wait()
        with counter_lock:
            local_buzzer_batch = batch.copy()
            publish_data_counter = 0
            batch.clear()
        publish.multiple(local_buzzer_batch, hostname=HOSTNAME, port=PORT)
        event.clear()

publish_event = threading.Event()
publisher_thread = threading.Thread(target=publisher_task, args=(publish_event, buzzer_batch))
publisher_thread.daemon = True
publisher_thread.start()


def db_callback(publish_event, settings, code, verbose=False):
    global publish_data_counter, publish_data_limit
    t = time.localtime()
    print("Buzzing " + code + "\n" )
    if verbose:
        t = time.localtime()
        print("=" * 20)
    buzzer_payload = {
        "measurement": "Buzzer",
        "simulated": settings['simulated'],
        "runs_on": settings["runs_on"],
        "name": settings["name"],
        "value": str(datetime.now())
    }

    with counter_lock:
        buzzer_batch.append(('Buzzer', json.dumps(buzzer_payload), 0, True))
        publish_data_counter += 1

    if publish_data_counter >= publish_data_limit:
        publish_event.set()


def run_db(settings, threads, stop_event, code):
    if settings['simulated']:
        db_thread = threading.Thread(target=db_callback, args=(publish_event, settings, code))
        db_thread.start()
        threads.append(db_thread)
    else:
        pin = settings['pin']
        db_thread = threading.Thread(target=buzz, args=pin)
        db_thread.start()
        threads.append(db_thread)
