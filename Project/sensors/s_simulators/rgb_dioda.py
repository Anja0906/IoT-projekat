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
    print(f"Color: {color_name}")

def run_rgb_dioda_simulation():
    try:
        generator = generate_values()
        while True:
            value = next(generator)
            print_color(value)
            time.sleep(1)
    except KeyboardInterrupt:
        print("Simulation stopped.")

