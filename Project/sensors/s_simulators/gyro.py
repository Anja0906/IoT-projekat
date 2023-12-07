import time
import random

def generate_gyro_data():
    while True:
        gyro_x = random.uniform(-100, 100)  # Simulate values in degrees per second
        gyro_y = random.uniform(-100, 100)
        gyro_z = random.uniform(-100, 100)
        yield gyro_x, gyro_y, gyro_z


def simulate_gyroscope(delay, callback, stop_event, publish_event, settings, code):
    for gyro_data in generate_gyro_data():
        callback(gyro_data, publish_event, settings, code)
        time.sleep(delay)
        if stop_event.is_set():
            break
