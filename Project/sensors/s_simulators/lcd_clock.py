import time
import random

def generate_time_values():
    while True:
        time_value = f"{random.randint(0, 23):02}{random.randint(0, 59):02}"
        yield time_value

def run_display_simulator(delay, callback, stop_event, publish_event, settings, code):
    for time_value in generate_time_values():
        time.sleep(delay)
        callback(time_value, publish_event, settings, code)
        if stop_event.is_set():
            break


