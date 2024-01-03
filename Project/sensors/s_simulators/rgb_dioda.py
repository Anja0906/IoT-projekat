import time
import random

from sensors.s_simulators.ir_receiver import get_current_button_name

ButtonsNames = ["LEFT", "RIGHT", "UP", "DOWN", "2", "3", "1", "OK", "4", "5", "6", "7", "8", "9", "*", "0",
                "#"]
def print_color(value):
    colors = {
        "0": "Off",
        "1": "White",
        "2": "Red",
        "3": "Green",
        "4": "Blue",
        "5": "Yellow",
        "6": "Purple",
        "7": "Light Blue"
    }
    return colors.get(value, "Unknown")

def run_rgb_dioda_simulation(delay, callback, ir_changed_event, publish_event, settings, code):
    while True:
        ir_changed_event.wait()
        color = print_color(get_current_button_name())
        if color != "Unknown":
            callback(color, publish_event, settings, code)
        print(color + "----------------------------")
        time.sleep(delay)
        ir_changed_event.clear()