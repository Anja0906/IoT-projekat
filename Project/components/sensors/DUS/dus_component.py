import threading
import json
import paho.mqtt.publish as publish
from components.broker_settings import HOSTNAME, PORT
from components.sensors.DUS.dus_simulation import run_uds_simulator

dus_batch = []
publish_data_counter = 0
publish_data_limit = 5
counter_lock = threading.Lock()
broj_osoba_u_sobi = 0


def publisher_task(event, dus_batch):
    global publish_data_counter, publish_data_limit
    while True:
        event.wait()
        with counter_lock:
            local_dus_batch = dus_batch.copy()
            publish_data_counter = 0
            dus_batch.clear()
        publish.multiple(local_dus_batch, hostname=HOSTNAME, port=PORT)
        event.clear()


publish_event = threading.Event()
publisher_thread = threading.Thread(target=publisher_task, args=(publish_event, dus_batch))
publisher_thread.daemon = True
publisher_thread.start()


def dus_callback(distance, publish_event, settings):
    global publish_data_counter, publish_data_limit

    dus_payload = {
        "measurement": "DoorUltraSonic",
        "simulated": settings['simulated'],
        "runs_on": settings["runs_on"],
        "name": settings["name"],
        "value": distance
    }
    with counter_lock:
        dus_batch.append(('Temperature', json.dumps(dus_payload), 0, True))
        publish_data_counter += 1

    if publish_data_counter >= publish_data_limit:
        publish_event.set()


def run_dus(settings, threads, code):
    if settings['simulated']:
        print("Starting " + code + " simulator")
        dus_thread = threading.Thread(target=run_uds_simulator,
                                      args=(5, dus_callback, publish_event, settings, code))
        dus_thread.start()
        threads.append(dus_thread)
        print(code + " simulator started\n")
    else:
        from components.sensors.DUS.dus_pi import run_uds
        print("Starting " + code + " loop")
        dus_thread = threading.Thread(target=run_uds, args=(
            settings['pin_trig'], settings['pin_echo'], 2, dus_callback, publish_event, settings, code))
        dus_thread.start()
        threads.append(dus_thread)
        print(code + " loop started")
