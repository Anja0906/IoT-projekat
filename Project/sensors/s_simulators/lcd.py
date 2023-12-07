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


def simulate_lcd_display(delay, callback, stop_event, publish_event, settings, code):
    for text in generate_display_text():
        time.sleep(delay)
        callback(text, publish_event, settings, code)
        if stop_event.is_set():
            break


