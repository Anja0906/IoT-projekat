import time
import random

keys = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "*", "#", "A", "B", "C", "D"]
pin = "1234"


def generate_values():
    while True:
        if random.randint(0, 10) != 0:
            length = random.randint(4, 8)
            code = ''.join(random.choices(keys, k=length))
        else:
            code = pin
        yield code

def run_ms_simulator(delay, callback, stop_event, publish_event, settings):
    for code in generate_values():
        time.sleep(delay) 
        callback(code, publish_event, settings)
        if stop_event.is_set():
            break
