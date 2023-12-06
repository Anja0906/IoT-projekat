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

def dus_callback(distance, publish_event, settings, code, verbose=False):
    global publish_data_counter, publish_data_limit
    if verbose:
        t = time.localtime()
        print("=" * 20)
        print(f"Timestamp: {time.strftime('%H:%M:%S', t)}")
        print(f"Code: {code}")
        print(f"Distance: " + str(distance) + " cm")
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


def run_dus(settings, threads, stop_event, code):
    if settings['simulated']:
        print("Starting " + code + " simulator")
        dus_thread = threading.Thread(target=run_uds_simulator, args=(5, dus_callback, stop_event, publish_event, settings, code))
        dus_thread.start()
        threads.append(dus_thread)
        print(code + " simulator started\n")
    else:
        from sensors.s_components.ultrasonic_sensor import get_distance
        print("Starting " + code + " loop")
        pin_trig = settings['pin_trig']
        pin_echo = settings['pin_echo']
        dus_thread = threading.Thread(target=get_distance, args=(pin_trig, pin_echo, code))
        dus_thread.start()
        threads.append(dus_thread)
        print(code + " loop started")
