import time
import random


def generate_value():
    while True:
        rnd = random.randint(0, 1)
        yield rnd


def run_ds_simulator(delay, callback, stop_event, code, print_lock):
    for motion in generate_value():
        time.sleep(delay)
        callback(motion, code, print_lock)
        if stop_event.is_set():
            break