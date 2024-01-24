import threading
import time
import json
import paho.mqtt.publish as publish

from components.broker_settings import HOSTNAME, PORT
from components.sensors.PIR.pir_simulation import run_pir_simulator

pir_batch = []
publish_data_counter = 0
publish_data_limit = 5
counter_lock = threading.Lock()
broj_osoba_u_sobi = 0

def publisher_task(event, batch):
    global publish_data_counter, publish_data_limit
    while True:
        event.wait()
        with counter_lock:
            local_pir_batch = batch.copy()
            publish_data_counter = 0
            batch.clear()
        publish.multiple(local_pir_batch, hostname=HOSTNAME, port=PORT)
        event.clear()


publish_event = threading.Event()
publisher_thread = threading.Thread(target=publisher_task, args=(publish_event, pir_batch))
publisher_thread.daemon = True
publisher_thread.start()


def dpir_callback(motion_detected, code, motion_detected_event, publish_event, dht_settings):
    global publish_data_counter, publish_data_limit
    if motion_detected:
        motion_detected_event.set()
        print("Desio se pokret na " + str(code))
        if code.startswith("RPIR"):
            if broj_osoba_u_sobi <= 0:
                print("ALAAARM na RPIRu\n")
                print(f"Broj osoba: {broj_osoba_u_sobi}")

    pir_payload = {
        "measurement": "Motion",
        "simulated": dht_settings['simulated'],
        "runs_on": dht_settings["runs_on"],
        "name": dht_settings["name"],
        "value": motion_detected
    }
    with counter_lock:
        pir_batch.append(('Motion', json.dumps(pir_payload), 0, True))
        publish_data_counter += 1
    if publish_data_counter >= publish_data_limit:
        publish_event.set()


def run_dpir(settings, threads, motion_detected_event, code,client):
    if settings['simulated']:
        print("Starting " + code + " simulator")
        dpir_thread = threading.Thread(target=run_pir_simulator,
                                       args=(15, dpir_callback, motion_detected_event, publish_event, settings, code))
        dpir_thread.start()
        threads.append(dpir_thread)
        print(code + " simulator started\n")
    else:
        from components.sensors.PIR.pir_pi import run_motion
        print("Starting " + code + " loop")
        pin = settings['pin']
        pir_thread = threading.Thread(target=run_motion, args=(
        pin, 2, dpir_callback, motion_detected_event, publish_event, settings, code))
        pir_thread.start()
        threads.append(pir_thread)
        print(code + " loop started")
