import time
import random

SimulatedButtons = [0x300ff22dd, 0x300ffc23d, 0x300ff629d, 0x300ffa857, 0x300ff9867, 0x300ffb04f, 0x300ff6897,
                    0x300ff02fd, 0x300ff30cf, 0x300ff18e7, 0x300ff7a85, 0x300ff10ef, 0x300ff38c7, 0x300ff5aa5,
                    0x300ff42bd, 0x300ff4ab5, 0x300ff52ad]
ButtonsNames = ["LEFT", "RIGHT", "UP", "DOWN", "2", "3", "1", "OK", "4", "5", "6", "7", "8", "9", "*", "0",
                "#"]


def generate_values():
    while True:
        yield random.choice(SimulatedButtons)


def get_button_name(button_hex):
    index = SimulatedButtons.index(button_hex)
    button_name = ButtonsNames[index] if index < len(ButtonsNames) else "Unknown"
    return button_name


def run_simulation(delay, callback, stop_event, publish_event, settings, code):
    for value in generate_values():
        time.sleep(delay)
        button = get_button_name(value)
        callback(button, publish_event, settings, code)
        if stop_event.is_set():
            break
