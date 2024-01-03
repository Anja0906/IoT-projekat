import threading
import json
import paho.mqtt.publish as publish
from sensors.broker_settings import HOSTNAME, PORT

from sensors.s_simulators.rgb_dioda import run_rgb_dioda_simulation
rgb_batch = []
publish_data_counter = 0
publish_data_limit = 5
counter_lock = threading.Lock()
rgb_state = False

def rgb_callback(color, publish_event, settings, code):
    global publish_data_counter, publish_data_limit, rgb_state
    if color == "Off":
        rgb_state = False
    else:
        rgb_state = True
        rgb_payload = {
            "measurement": "RGB",
            "simulated": settings['simulated'],
            "runs_on": settings["runs_on"],
            "name": settings["name"],
            "value": color
        }
        with counter_lock:
            rgb_batch.append(('RGB', json.dumps(rgb_payload), 0, True))
            publish_data_counter += 1

    if publish_data_counter >= publish_data_limit:
        publish_event.set()

def publisher_task(event, batch):
    global publish_data_counter, publish_data_limit
    while True:
        event.wait()
        with counter_lock:
            local_rgb_batch = batch.copy()
            publish_data_counter = 0
            batch.clear()
        publish.multiple(local_rgb_batch, hostname=HOSTNAME, port=PORT)
        event.clear()


publish_event = threading.Event()
publisher_thread = threading.Thread(target=publisher_task, args=(publish_event, rgb_batch))
publisher_thread.daemon = True
publisher_thread.start()


def run_rgb_light(settings, threads, ir_changed_event, code):
    if settings['simulated']:
        print("Starting " + code + " simulator")
        rgb_thread = threading.Thread(target=run_rgb_dioda_simulation, args=(5, rgb_callback, ir_changed_event, publish_event, settings, code))
        rgb_thread.start()
        threads.append(rgb_thread)
        print(code + " simulator started\n")
    else:
        from sensors.s_components.rgb_dioda import run_rgb_dioda
        print("Starting " + code + " loop")
        rgb_thread = threading.Thread(target=run_rgb_dioda, args=(5, rgb_callback, ir_changed_event, publish_event, settings, code))
        rgb_thread.start()
        threads.append(rgb_thread)
        print(code + " loop started")