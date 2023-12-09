import threading
import time
import json
import paho.mqtt.publish as publish
from sensors.broker_settings import HOSTNAME, PORT

door_open = False
ds_batch = []
publish_data_counter = 0
publish_data_limit = 5
counter_lock = threading.Lock()

def publisher_task(event, ds_batch):
    global publish_data_counter, publish_data_limit
    while True:
        event.wait()
        with counter_lock:
            local_ds_batch = ds_batch.copy()
            publish_data_counter = 0
            ds_batch.clear()
        publish.multiple(local_ds_batch, hostname=HOSTNAME, port=PORT)
        event.clear()


publish_event = threading.Event()
publisher_thread = threading.Thread(target=publisher_task, args=(publish_event, ds_batch))
publisher_thread.daemon = True
publisher_thread.start()


def ds_callback(motion, publish_event, settings, code, verbose=False):
    global door_open, publish_data_counter, publish_data_limit
    if verbose:
        t = time.localtime()
        print("=" * 20)
        print(f"Timestamp: {time.strftime('%H:%M:%S', t)}")
        print(f"Code: {code}")
        if door_open:
            door_open = not door_open
            print("Door is currently opened")
        else:
            door_open = not door_open
            print("Door is currently closed")
    door_sensor_payload = {
        "measurement": "DoorSensor",
        "simulated": settings['simulated'],
        "runs_on": settings["runs_on"],
        "name": settings["name"],
        "value": motion==1
    }

    with counter_lock:
        ds_batch.append(('DoorSensor', json.dumps(door_sensor_payload), 0, True))
        publish_data_counter += 1

    if publish_data_counter >= publish_data_limit:
        publish_event.set()


def run_ds(settings, threads, stop_event, code):
    if settings['simulated']:
        from sensors.s_simulators.door_sensor import run_ds_simulator
        print("Starting " + code + " simulator")
        ds_thread = threading.Thread(target=run_ds_simulator, args=(2, ds_callback, stop_event, publish_event, settings, code))
        ds_thread.start()
        threads.append(ds_thread)
        print(code + " simulator started\n")
    else:
        from sensors.s_components.door_sensor_button import press_button
        print("Starting " + code + " loop")
        pin = settings['pin']
        ds_thread = threading.Thread(target=press_button, args=(pin, ds_callback, stop_event, publish_event, settings, code))
        ds_thread.start()
        threads.append(ds_thread)
        print(code + " loop started")
