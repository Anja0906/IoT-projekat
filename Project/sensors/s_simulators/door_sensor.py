import time
import random


def generate_value():
    while True:
        rnd = random.randint(0, 1)
        yield rnd


def run_ds_simulator(delay, callback, stop_event, publish_event, settings, code):
        generator = generate_value()
        while True:
            motion = next(generator)
            time.sleep(delay)
            callback(motion, publish_event, settings, code)