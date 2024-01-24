import random
import time


def generate_values():
    while True:
        motion_detected = random.choice([True, False])
        yield motion_detected


def run_pir_simulator(delay, callback, motion_detected_event, publish_event, settings, code):
    for motion in generate_values():
        time.sleep(delay)
        callback(motion, code, motion_detected_event, publish_event, settings)
