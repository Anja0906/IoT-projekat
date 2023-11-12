import random
import time


def generate_key_presses(max_length=8):
    while True:
        key_presses = [str(random.randint(0, 9)) for _ in range(random.randint(1, max_length))]
        yield ''.join(key_presses)


def run_keypad_simulator(delay, callback, stop_event, code, print_lock):
    for key_sequence in generate_key_presses():
        time.sleep(delay)
        callback(key_sequence, code, print_lock)
        if stop_event.is_set():
            break


def keypad_callback(key_sequence, code):
    print(f"Uneta šifra: {key_sequence}")
