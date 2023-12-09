import threading
import json
import paho.mqtt.publish as publish
from sensors.broker_settings import HOSTNAME, PORT

from sensors.s_simulators.lcd import simulate_lcd_display

lcd_batch = []
publish_data_counter = 0
publish_data_limit = 5
counter_lock = threading.Lock()


def display_callback(text, publish_event, settings, code, verbose=False):
    global publish_data_counter, publish_data_limit
    if verbose:
        print(f"Prikazani tekst: {text}")
    lcd_payload = {
        "measurement": "LCD",
        "simulated": settings['simulated'],
        "runs_on": settings["runs_on"],
        "name": settings["name"],
        "value": text
    }
    with counter_lock:
        lcd_batch.append(('LCD', json.dumps(lcd_payload), 0, True))
        publish_data_counter += 1

    if publish_data_counter >= publish_data_limit:
        publish_event.set()


def publisher_task(event, batch):
    global publish_data_counter, publish_data_limit
    while True:
        event.wait()
        with counter_lock:
            local_lcd_batch = batch.copy()
            publish_data_counter = 0
            batch.clear()
        publish.multiple(local_lcd_batch, hostname=HOSTNAME, port=PORT)
        event.clear()


publish_event = threading.Event()
publisher_thread = threading.Thread(target=publisher_task, args=(publish_event, lcd_batch))
publisher_thread.daemon = True
publisher_thread.start()


def run_lcd(settings, threads, stop_event, code):
    if settings['simulated']:
        print("Starting " + code + " simulator")
        lcd_thread = threading.Thread(target=simulate_lcd_display,
                                      args=(2, display_callback, stop_event, publish_event, settings, code))
        lcd_thread.start()
        threads.append(lcd_thread)
        print(code + " simulator started\n")
    else:
        from sensors.s_components.lcd.LCD1602 import run_clock_component
        print("Starting " + code + " loop")
        dms_thread = threading.Thread(target=run_clock_component, args=(2, display_callback, stop_event, publish_event, settings, code))
        dms_thread.start()
        threads.append(dms_thread)
        print(code + " loop started")
