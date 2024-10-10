import time
import random


def generate_values():
    while True:
        accel_x = random.uniform(-32768, 32767)
        gyro_x = random.uniform(-32768, 32767)
        accel_y = random.uniform(-32768, 32767)
        gyro_y = random.uniform(-32768, 32767)
        accel_z = random.uniform(-32768, 32767)
        gyro_z = random.uniform(-32768, 32767)
        accel_tuple = (accel_x, accel_y, accel_z)
        gyro_tuple = (gyro_x, gyro_y, gyro_z)
        yield accel_tuple, gyro_tuple


def run_gyro_simulator(delay, callback, stop_event, publish_event, settings):
    for accel, gyro in generate_values():
        callback(accel, gyro, publish_event, settings)
        if stop_event.is_set():
            break
        time.sleep(delay)
