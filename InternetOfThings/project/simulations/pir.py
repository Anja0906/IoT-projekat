import random
import time


def generate_value():
    return random.randint(0, 1) == 1

def run_pir_simulator(delay, callback, stop_event, publish_event, settings):
    while True:
        motion_detected = generate_value()
        time.sleep(delay) 
        if motion_detected:
            callback(publish_event, settings, 1)
        else:
            callback(publish_event, settings, 0)
        if stop_event.is_set():
            break
