import threading
import json
import paho.mqtt.publish as publish
from components.broker_settings import HOSTNAME, PORT

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


def ds_callback(stop_event,motion, publish_event, settings, code):
    global door_open, publish_data_counter, publish_data_limit
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
        #TODO: Uraditi slanje mqtt na server kad god se detektuje pokret da se proveri poslednjih 5 sekundi i aktivira alarm
    stop_event.clear()

def run_ds(settings, threads, stop_event, code, client):
    if settings['simulated']:
        from components.sensors.Button.button_simulation import run_ds_simulator
        print("Starting " + code + " simulator")
        ds_thread = threading.Thread(target=run_ds_simulator, args=(0.7, ds_callback, stop_event, publish_event, settings, code, client))
        ds_thread.start()
        threads.append(ds_thread)
        print(code + " simulator started\n")
    else:
        from components.sensors.Button.button_pi import press_button
        print("Starting " + code + " loop")
        pin = settings['pin']
        ds_thread = threading.Thread(target=press_button, args=(pin, ds_callback, stop_event, publish_event, settings, code, client))
        ds_thread.start()
        threads.append(ds_thread)
        print(code + " loop started")
