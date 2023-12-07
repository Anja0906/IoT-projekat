import threading
import time
import random
import string


def generate_random_characters(length):
    characters = string.ascii_letters + string.digits + string.punctuation + string.whitespace
    return ''.join(random.choice(characters) for _ in range(length))


def generate_display_text():
    while True:
        text = generate_random_characters(16)  # Generiše nasumični tekst od 16 karaktera
        yield text


def display_callback(text):
    print(f"Prikazani tekst: {text}")


def simulate_lcd_display(delay, stop_event):
    for text in generate_display_text():
        time.sleep(delay)
        display_callback(text)
        if stop_event.is_set():
            break


