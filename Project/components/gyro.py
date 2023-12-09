import threading
import json
import paho.mqtt.publish as publish
from sensors.broker_settings import HOSTNAME, PORT

from sensors.s_simulators.gyro import simulate_gyroscope

gyro_batch = []
publish_data_counter = 0
publish_data_limit = 5
counter_lock = threading.Lock()


def publisher_task(event, batch):
    global publish_data_counter, publish_data_limit
    while True:
        event.wait()
        with counter_lock:
            local_gyro_batch = batch.copy()
            publish_data_counter = 0
            batch.clear()
        publish.multiple(local_gyro_batch, hostname=HOSTNAME, port=PORT)
        event.clear()


publish_event = threading.Event()
publisher_thread = threading.Thread(target=publisher_task, args=(publish_event, gyro_batch))
publisher_thread.daemon = True
publisher_thread.start()

def gyro_callback(data, publish_event, settings, code, verbose=False):
    global publish_data_counter, publish_data_limit
    accel_x, accel_y, accel_z, gyro_x, gyro_y, gyro_z = data
    load = "a/g:%.2f g\t%.2f g\t%.2f g\t%.2f d/s\t%.2f d/s\t%.2f d/s"%(accel_x/16384.0,accel_y/16384.0,
            accel_z/16384.0,gyro_x/131.0,gyro_y/131.0,gyro_z/131.0)
    if verbose:
        print("a/g:%.2f g\t%.2f g\t%.2f g\t%.2f d/s\t%.2f d/s\t%.2f d/s"%(accel_x/16384.0,accel_y/16384.0,
            accel_z/16384.0,gyro_x/131.0,gyro_y/131.0,gyro_z/131.0))
    gyro_payload = {
        "measurement": "Gyro",
        "simulated": settings['simulated'],
        "runs_on": settings["runs_on"],
        "name": settings["name"],
        "value": load
    }

    with counter_lock:
        gyro_batch.append(('Gyro', json.dumps(gyro_payload), 0, True))
        publish_data_counter += 1

    if publish_data_counter >= publish_data_limit:
        publish_event.set()

def run_gyro(settings, threads, stop_event, code):
    if settings['simulated']:
        print("Starting " + code + " simulator")
        gyro_thread = threading.Thread(target=simulate_gyroscope, args=(2, gyro_callback, stop_event, publish_event, settings, code))
        gyro_thread.start()
        threads.append(gyro_thread)
        print(code + " simulator started\n")
    else:
        from sensors.s_components.MPU6050.gyro import gyro_run
        print("Starting " + code + " loop")
        gyro_thread = threading.Thread(target=gyro_run, args=(2, gyro_callback, stop_event, publish_event, settings, code))
        gyro_thread.start()
        threads.append(gyro_thread)
        print(code + " loop started")
