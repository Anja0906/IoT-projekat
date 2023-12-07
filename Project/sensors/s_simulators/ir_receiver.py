import time
import random

SimulatedButtons = [0x300ff22dd, 0x300ffc23d, 0x300ff629d, 0x300ffa857]
ButtonsNames = ["LEFT", "RIGHT", "UP", "DOWN"]


def generate_values():
    while True:
        yield random.choice(SimulatedButtons)


# Callback funkcija za ispis
def print_simulated_button(button_hex):
    index = SimulatedButtons.index(button_hex)
    button_name = ButtonsNames[index] if index < len(ButtonsNames) else "Unknown"
    print(f"Simulated Button Pressed: {button_name}")


def run_simulation():
    try:
        generator = generate_values()
        while True:
            button_hex = next(generator)
            print_simulated_button(button_hex)
            time.sleep(1)
    except KeyboardInterrupt:
        print("Simulation stopped.")


if __name__ == "__main__":
    print("Button Simulation is starting ... ")
    run_simulation()
