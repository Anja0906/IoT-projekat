import time
import random

def generate_gyro_data():
    while True:
        accel_x = random.uniform(-32768, 32767)  # Simulate values in degrees per second
        gyro_x = random.uniform(-32768, 32767)  # Simulate values in degrees per second
        accel_y = random.uniform(-32768, 32767)
        gyro_y = random.uniform(-32768, 32767)
        accel_z = random.uniform(-32768, 32767)
        gyro_z = random.uniform(-32768, 32767)
        yield accel_x, accel_y, accel_z, gyro_x, gyro_y, gyro_z


def simulate_gyroscope(delay, callback, publish_event, settings, code):
    generator = generate_gyro_data()
    while True:
        gyro_data = next(generator)
        time.sleep(delay)
        callback(gyro_data, publish_event, settings, code)
