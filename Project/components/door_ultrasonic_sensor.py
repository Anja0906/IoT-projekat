import threading
import time
import json
import paho.mqtt.publish as publish
from sensors.broker_settings import HOSTNAME, PORT
from sensors.s_simulators.ultrasonic_sensor import run_uds_simulator

dus_batch = []
publish_data_counter = 0
publish_data_limit = 5
counter_lock = threading.Lock()
broj_osoba_u_sobi1, ulazak_ili_izlazak, broj_osoba_u_sobi2 = 0, "ulazak", 0


def publisher_task(event, dht_batch):
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


def dus_control_thread(distance, publish_event, settings, code):
    global broj_osoba_u_sobi1, ulazak_ili_izlazak, broj_osoba_u_sobi2

    if code == "DUS1":
        if distance < 150:
            broj_osoba_u_sobi1 += 1
            print("Trenutni broj osoba u sobi 1: ", broj_osoba_u_sobi1)
        else:
            broj_osoba_u_sobi1 = max(0, broj_osoba_u_sobi1 - 1)
            print("Trenutni broj osoba u sobi 1: ", broj_osoba_u_sobi1)
    else:
        if distance < 150:
            broj_osoba_u_sobi2 += 1
            print("Trenutni broj osoba u sobi 2: ", broj_osoba_u_sobi2)
        else:
            broj_osoba_u_sobi2 = max(0, broj_osoba_u_sobi2 - 1)
            print("Trenutni broj osoba u sobi 2: ", broj_osoba_u_sobi2)

    dus_callback(distance, publish_event, settings)


def run_dus(settings, threads, stop_event, code):
    if settings['simulated']:
        print("Starting " + code + " simulator")
        dus_thread = threading.Thread(target=run_uds_simulator,
                                      args=(1, dus_control_thread, stop_event, publish_event, settings, code))
        dus_thread.start()
        threads.append(dus_thread)
        print(code + " simulator started\n")
    else:
        from sensors.s_components.ultrasonic_sensor import run_uds
        print("Starting " + code + " loop")
        pin_trig = settings['pin_trig']
        pin_echo = settings['pin_echo']
        dus_thread = threading.Thread(target=run_uds, args=(
            pin_trig, pin_echo, 5, dus_callback, stop_event, publish_event, settings, code))
        dus_thread.start()
        threads.append(dus_thread)
        print(code + " loop started")
