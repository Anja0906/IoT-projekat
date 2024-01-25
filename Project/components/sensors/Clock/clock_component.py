import threading
import json
import time
from datetime import datetime

import paho.mqtt.publish as publish
import paho.mqtt.client as mqtt
from components.broker_settings import HOSTNAME, PORT
from components.sensors.Clock.clock_simulation import run_display_simulator
is_set = False
is_turned_off = False
alarm_time = datetime(2025, 2, 1, 22, 0).time()
clock_batch = []
publish_data_counter = 0
publish_data_limit = 5
counter_lock = threading.Lock()

mqtt_client = mqtt.Client()
mqtt_client.connect(HOSTNAME, PORT, 60)
mqtt_client.loop_start()
mqtt_client.subscribe("clock")
mqtt_client.subscribe("clock_turn_off")
def on_message(client, userdata, msg):
    global alarm_time, is_set, is_turned_off
    if msg.topic == "clock":
        data = msg.payload.decode()
        parsed_time = datetime.strptime(data, "%H:%M").time()
        is_set = True
        is_turned_off = False  # Resetujte is_turned_off svaki put kada se postavi novi alarm
        alarm_time = parsed_time
    elif msg.topic == "clock_turn_off":
        mqtt_client.publish("budilnik/off", "")
        is_turned_off = True
        is_set = False

mqtt_client.on_message = on_message

def display_callback(time, publish_event, settings, code):
    global publish_data_counter, publish_data_limit
    print("Vreme je: " + time)
    clock_payload = {
        "measurement": "Clock",
        "simulated": settings['simulated'],
        "runs_on": settings["runs_on"],
        "name": settings["name"],
        "value": time
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

def clock_awaiter(delay, alarm_event):
    global is_set, is_turned_off
    while True:
        current_time = datetime.now().time()
        if is_set and not is_turned_off and alarm_time <= current_time:
            print("BUDILNIIIIK")
            alarm_event.set()
            is_set = True  # Postavite is_set na False nakon aktiviranja alarma
            mqtt_client.publish("budilnik/on","")
        else:
            alarm_event.clear()
        time.sleep(delay)

def run_clock(settings, threads, alarm_event, code):
    clock_wait_thread = threading.Thread(target=clock_awaiter,
                                         args=(1, alarm_event))
    clock_wait_thread.start()
    threads.append(clock_wait_thread)
    if settings['simulated']:
        print("Starting " + code + " simulator")
        clock_thread = threading.Thread(target=run_display_simulator,
                                      args=(1, display_callback, alarm_event, publish_event, settings, code))
        clock_thread.start()
        threads.append(clock_thread)
        print(code + " simulator started\n")
    else:
        from clock_pi import run_clock
        print("Starting " + code + " loop")
        dms_thread = threading.Thread(target=run_clock,
                                      args=(2, display_callback, alarm_event, publish_event, settings, code))
        dms_thread.start()
        threads.append(dms_thread)
        print(code + " loop started")
