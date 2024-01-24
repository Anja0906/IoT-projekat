from components.sensors.DHT.dht_simulation import run_dht_simulator
import threading
import json
import paho.mqtt.publish as publish
from components.broker_settings import HOSTNAME, PORT

dht_batch = []
publish_data_counter = 0
publish_data_limit = 5
counter_lock = threading.Lock()
lcd_txt = ""

def publisher_task(event, dht_batch):
    global publish_data_counter, publish_data_limit
    while True:
        event.wait()
        with counter_lock:
            local_dht_batch = dht_batch.copy()
            publish_data_counter = 0
            dht_batch.clear()
        publish.multiple(local_dht_batch, hostname=HOSTNAME, port=PORT)
        event.clear()


publish_event = threading.Event()
publisher_thread = threading.Thread(target=publisher_task, args=(publish_event, dht_batch))
publisher_thread.daemon = True
publisher_thread.start()

def get_lcd_text():
    return lcd_txt

def dht_callback(humidity, temperature, publish_event, dht_settings, code):
    global publish_data_counter, publish_data_limit, lcd_txt
    temp_payload = {
        "measurement": "Temperature",
        "simulated": dht_settings['simulated'],
        "runs_on": dht_settings["runs_on"],
        "name": dht_settings["name"],
        "value": temperature
    }

    humidity_payload = {
        "measurement": "Humidity",
        "simulated": dht_settings['simulated'],
        "runs_on": dht_settings["runs_on"],
        "name": dht_settings["name"],
        "value": humidity
    }

    if code == "GDHT":
        lcd_txt = str(temperature)+"°C"+ " " + str(humidity)+"%"

    with counter_lock:
        dht_batch.append(('Temperature', json.dumps(temp_payload), 0, True))
        dht_batch.append(('Humidity', json.dumps(humidity_payload), 0, True))
        publish_data_counter += 1

    if publish_data_counter >= publish_data_limit:
        publish_event.set()


def run_dht(settings, threads, code,client):
    if settings['simulated']:
        print("Starting " + code + " simulator")
        dht_thread = threading.Thread(target = run_dht_simulator, args=(9, dht_callback, publish_event, settings, code))
        dht_thread.start()
        threads.append(dht_thread)
        print(code + " simulator started\n")
    else:
        from components.sensors.DHT.dht_pi import run_dht_loop
        from components.sensors.DHT.dht_pi import DHT
        print("Starting " + code + " loop")
        dht = DHT(settings['pin'])
        dht_thread = threading.Thread(target=run_dht_loop, args=(dht, 2, dht_callback, publish_event, settings))
        dht_thread.start()
        threads.append(dht_thread)
        print(code + " loop started")
