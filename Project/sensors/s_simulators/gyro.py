import threading
import time
import random

def generate_gyro_data():
    while True:
        gyro_x = random.uniform(-100, 100)  # Simulate values in degrees per second
        gyro_y = random.uniform(-100, 100)
        gyro_z = random.uniform(-100, 100)
        yield gyro_x, gyro_y, gyro_z

def gyroscope_callback(data, publish_event, settings):
    gyro_x, gyro_y, gyro_z = data
    print(f"Gyroscope X: {gyro_x:.2f} d/s, Y: {gyro_y:.2f} d/s, Z: {gyro_z:.2f} d/s")

def simulate_gyroscope(callback, stop_event, publish_event, settings):
    for gyro_data in generate_gyro_data():
        callback(gyro_data, publish_event, settings)
        time.sleep(1)
        if stop_event.is_set():
            break

if __name__ == '__main__':
    print("Gyroscope Simulation is starting ... ")
    try:
        simulate_gyroscope(gyroscope_callback, stop_event=threading.Event(), publish_event=None, settings=None)
    except KeyboardInterrupt:
        pass
