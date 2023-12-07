import threading
import json
import paho.mqtt.publish as publish
from sensors.broker_settings import HOSTNAME, PORT
from sensors.s_simulators.lcd_clock import run_display_simulator

clock_batch = []
publish_data_counter = 0
publish_data_limit = 5
counter_lock = threading.Lock()


def display_callback(time_value, publish_event, settings, code, verbose=False):
    global publish_data_counter, publish_data_limit
    load = f"{time_value[0:2]}:{time_value[2:4]}"
    if verbose:
        print(f"{time_value[0:2]}:{time_value[2:4]}")
    clock_payload = {
        "measurement": "Clock",
        "simulated": settings['simulated'],
        "runs_on": settings["runs_on"],
        "name": settings["name"],
        "value": load
    }
    with counter_lock:
        clock_batch.append(('Clock', json.dumps(clock_payload), 0, True))
        publish_data_counter += 1

    if publish_data_counter >= publish_data_limit:
        publish_event.set()


def publisher_task(event, batch):
    global publish_data_counter, publish_data_limit
    while True:
        event.wait()
        with counter_lock:
            local_clock_batch = batch.copy()
            publish_data_counter = 0
            batch.clear()
        publish.multiple(local_clock_batch, hostname=HOSTNAME, port=PORT)
        event.clear()


publish_event = threading.Event()
publisher_thread = threading.Thread(target=publisher_task, args=(publish_event, clock_batch))
publisher_thread.daemon = True
publisher_thread.start()


def run_clock(settings, threads, stop_event, code):
    if settings['simulated']:
        print("Starting " + code + " simulator")
        lcd_thread = threading.Thread(target=run_display_simulator,
                                      args=(2, display_callback, stop_event, publish_event, settings, code))
        lcd_thread.start()
        threads.append(lcd_thread)
        print(code + " simulator started\n")
    else:
        from sensors.s_components.lcd.LCD1602 import run_clock_component
        print("Starting " + code + " loop")
        dms_thread = threading.Thread(target=run_clock_component, args=())
        dms_thread.start()
        threads.append(dms_thread)
        print(code + " loop started")
