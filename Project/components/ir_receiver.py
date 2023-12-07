import threading
import json
import paho.mqtt.publish as publish
from sensors.broker_settings import HOSTNAME, PORT

from sensors.s_simulators.ir_receiver import run_simulation

bir_batch = []
publish_data_counter = 0
publish_data_limit = 5
counter_lock = threading.Lock()


def bir_callback(button_name, publish_event, settings, code, verbose=False):
    global publish_data_counter, publish_data_limit
    if verbose:
        print(f"Pritisnuto dugme: {button_name}")
    bir_payload = {
        "measurement": "BedroomInfrared",
        "simulated": settings['simulated'],
        "runs_on": settings["runs_on"],
        "name": settings["name"],
        "value": button_name
    }
    with counter_lock:
        bir_batch.append(('BedroomInfrared', json.dumps(bir_payload), 0, True))
        publish_data_counter += 1

    if publish_data_counter >= publish_data_limit:
        publish_event.set()

def publisher_task(event, batch):
    global publish_data_counter, publish_data_limit
    while True:
        event.wait()
        with counter_lock:
            local_bir_batch = batch.copy()
            publish_data_counter = 0
            batch.clear()
        publish.multiple(local_bir_batch, hostname=HOSTNAME, port=PORT)
        event.clear()


publish_event = threading.Event()
publisher_thread = threading.Thread(target=publisher_task, args=(publish_event, bir_batch))
publisher_thread.daemon = True
publisher_thread.start()
def run_ir_receiver(settings, threads, stop_event, code):
    if settings['simulated']:
        print("Starting " + code + " simulator")
        ir_thread = threading.Thread(target=run_simulation,args=(2, bir_callback, stop_event, publish_event, settings, code))
        ir_thread.start()
        threads.append(ir_thread)
        print(code + " simulator started\n")
    else:
        from sensors.s_components.ir_receiver import run_ir_receiver
        print("Starting " + code + " loop")
        ir_thread = threading.Thread(target=run_ir_receiver, args=())
        ir_thread.start()
        threads.append(ir_thread)
        print(code + " loop started")
