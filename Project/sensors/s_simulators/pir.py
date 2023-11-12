import random
import time


def generate_values():
    while True:
        motion_detected = random.choice([True, False])
        yield motion_detected


def run_pir_simulator(delay, callback, stop_event, code, print_lock):
    for motion in generate_values():
        time.sleep(delay)
        callback(motion, code, print_lock)
        if stop_event.is_set():
            break
