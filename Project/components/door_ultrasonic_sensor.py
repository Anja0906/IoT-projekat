import threading
import time
import json
import paho.mqtt.publish as publish
from sensors.broker_settings import HOSTNAME, PORT
from sensors.s_simulators.ultrasonic_sensor import run_uds_simulator
from server.querry_service import query_dus_sensor
from server.server import get_server_values

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


def dus_control_thread(distance, publish_event, pir_motion_detected_event, settings, read_from_db_event):
    dus_callback(distance, publish_event, settings)
    if pir_motion_detected_event.is_set():
        print("setuj read event")
        read_from_db_event.set()


def run_dus_checker(delay, read_from_db_event_dus, code):
    global broj_osoba_u_sobi
    while True:
        read_from_db_event_dus.wait()
        i_client, org = get_server_values()
        if query_dus_sensor(i_client, org, code):
            broj_osoba_u_sobi += 1
        else:
            broj_osoba_u_sobi = max(0, broj_osoba_u_sobi - 1)
        print(f"Citaj iz baze podataka na {code}")
        print(f"Broj osoba u sobi je  {broj_osoba_u_sobi}")
        time.sleep(delay)
        read_from_db_event_dus.clear()


def run_dus(settings, threads, pir_motion_detected_event, read_from_db_event, code):
    if settings['simulated']:
        print("Starting " + code + " simulator")
        dus_thread = threading.Thread(target=run_uds_simulator,
                                      args=(5, dus_control_thread, pir_motion_detected_event, publish_event, settings,
                                            read_from_db_event, code))
        dus_thread.start()
        dus_checker_thread = threading.Thread(target=run_dus_checker, args=(5, read_from_db_event, code))
        dus_checker_thread.start()
        threads.append(dus_thread)
        threads.append(dus_checker_thread)
        print(code + " simulator started\n")
    else:
        from sensors.s_components.ultrasonic_sensor import run_uds
        print("Starting " + code + " loop")
        pin_trig = settings['pin_trig']
        pin_echo = settings['pin_echo']
        dus_thread = threading.Thread(target=run_uds, args=(
            pin_trig, pin_echo, 5, dus_callback, pir_motion_detected_event, publish_event, settings, code))
        dus_thread.start()
        threads.append(dus_thread)
        print(code + " loop started")
