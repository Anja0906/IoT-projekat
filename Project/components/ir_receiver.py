import threading
import json
import paho.mqtt.publish as publish
from sensors.broker_settings import HOSTNAME, PORT

from sensors.s_simulators.ir_receiver import run_simulation


def gyro_callback(data, publish_event, settings, code, verbose=False):
    global publish_data_counter, publish_data_limit
    gyro_x, gyro_y, gyro_z = data
    load = f"Gyroscope {code} - X: {gyro_x:.2f} d/s, Y: {gyro_y:.2f} d/s, Z: {gyro_z:.2f} d/s"
    if verbose:
        print(f"Gyroscope {code} - X: {gyro_x:.2f} d/s, Y: {gyro_y:.2f} d/s, Z: {gyro_z:.2f} d/s")
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


def run_ir_receiver(settings, threads, stop_event, code):
    if settings['simulated']:
        print("Starting " + code + " simulator")
        ir_thread = threading.Thread(target=run_simulation(),args=())
        ir_thread.start()
        threads.append(ir_thread)
        print(code + " simulator started\n")
    else:
        from sensors.s_components.ir_receiver import run_ir_receiver
        print("Starting " + code + " loop")
        ir_thread = threading.Thread(target=run_ir_receiver, args=())
        ir_thread.start()
        threads.append(ir_thread)
        print(code + " loop started")
