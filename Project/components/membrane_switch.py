import threading
import time
from sensors.s_simulators.membrane_switch import run_keypad_simulator
import json
import paho.mqtt.publish as publish
from sensors.broker_settings import HOSTNAME, PORT

ms_batch = []
publish_data_counter = 0
publish_data_limit = 5
counter_lock = threading.Lock()

def publisher_task(event, batch):
    global publish_data_counter, publish_data_limit
    while True:
        event.wait()
        with counter_lock:
            local_ms_batch = ms_batch.copy()
            publish_data_counter = 0
            ms_batch.clear()
        publish.multiple(local_ms_batch, hostname=HOSTNAME, port=PORT)
        event.clear()

publish_event = threading.Event()
publisher_thread = threading.Thread(target=publisher_task, args=(publish_event, ms_batch))
publisher_thread.daemon = True
publisher_thread.start()

# key_sequence, publish_event, settings, code
def dms_callback(result, publish_event, settings, code, verbose=False):
    global publish_data_counter, publish_data_limit

    if verbose:
        t = time.localtime()
        print("=" * 20)
        print(f"Timestamp: {time.strftime('%H:%M:%S', t)}")
        print(f"Code: {code}")
        print(f"User entered: " + str(result))
    ms_payload = {
        "measurement": "MembraneSwitch",
        "simulated": settings['simulated'],
        "runs_on": settings["runs_on"],
        "name": settings["name"],
        "value": str(result)
    }

    with counter_lock:
        ms_batch.append(('MembraneSwitch', json.dumps(ms_payload), 0, True))
        publish_data_counter += 1

    if publish_data_counter >= publish_data_limit:
        publish_event.set()


def run_dms(settings, threads, stop_event, code):
    if settings['simulated']:
        print("Starting " + code + " simulator")
        dms_thread = threading.Thread(target=run_keypad_simulator,
                                      args=(5, dms_callback, stop_event, code, publish_event, settings))
        dms_thread.start()
        threads.append(dms_thread)
        print(code + " simulator started\n")
    else:
        from sensors.s_components.membrane_switch import detect_motion
        r1 = settings['R1']
        r2 = settings['R2']
        r3 = settings['R3']
        r4 = settings['R4']
        c1 = settings['C1']
        c2 = settings['C2']
        c3 = settings['C3']
        c4 = settings['C4']
        pir_thread = threading.Thread(target=detect_motion, args=(code, r1, r2, r3, r4, c1, c2, c3, c4, dms_callback, stop_event, publish_event, settings))
        pir_thread.start()
        threads.append(pir_thread)
