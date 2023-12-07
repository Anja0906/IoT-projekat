import threading
import time
import random

def generate_time_values():
    while True:
        time_value = f"{random.randint(0, 23):02}{random.randint(0, 59):02}"
        yield time_value

def display_callback(time_value):
    print(f"Prikazano vreme: {time_value[0:2]}:{time_value[2:4]}")

def run_display_simulator(delay, callback, stop_event):
    for time_value in generate_time_values():
        time.sleep(delay)
        callback(time_value)
        if stop_event.is_set():
            break

# stop_event = threading.Event()
# run_display_simulator(1, display_callback, stop_event)

