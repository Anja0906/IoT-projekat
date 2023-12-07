import threading
import time
import random

from sensors.s_components.MPU6050.gyro import gyro_run
from sensors.s_simulators.gyro import simulate_gyroscope


def gyro_callback(data, code):
    gyro_x, gyro_y, gyro_z = data
    print(f"Gyroscope {code} - X: {gyro_x:.2f} d/s, Y: {gyro_y:.2f} d/s, Z: {gyro_z:.2f} d/s")


def run_gyro(settings, threads, stop_event, code):
    if settings['simulated']:
        print("Starting " + code + " simulator")
        gyro_thread = threading.Thread(target=simulate_gyroscope, args=(gyro_callback, stop_event, settings, code))
        gyro_thread.start()
        threads.append(gyro_thread)
        print(code + " simulator started\n")
    else:
        print("Starting " + code + " loop")
        gyro_thread = threading.Thread(target=gyro_run, args=())
        gyro_thread.start()
        threads.append(gyro_thread)
        print(code + " loop started")
