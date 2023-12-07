import time
import random

def generate_values():
    while True:
        value = random.randint(0, 7)
        yield value

def print_color(value):
    colors = {
        0: "Off",
        1: "White",
        2: "Red",
        3: "Green",
        4: "Blue",
        5: "Yellow",
        6: "Purple",
        7: "Light Blue"
    }
    color_name = colors.get(value, "Unknown")
    return color_name

def run_rgb_dioda_simulation(delay, callback, stop_event, publish_event, settings, code):
    for value in generate_values():
        time.sleep(delay)
        color = print_color(value)
        callback(color, publish_event, settings, code)
        if stop_event.is_set():
            break

