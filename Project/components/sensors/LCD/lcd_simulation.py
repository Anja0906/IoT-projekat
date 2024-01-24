import time
import random
import string

from components.sensors.DHT.dht_component import get_lcd_text


def generate_random_characters(length):
    characters = string.ascii_letters + string.digits + string.punctuation + string.whitespace
    return ''.join(random.choice(characters) for _ in range(length))


def generate_display_text():
    while True:
        text = generate_random_characters(16)  # Generiše nasumični tekst od 16 karaktera
        yield text


def simulate_lcd_display(delay, callback, publish_event, settings, code):
    while True:
        lcd_txt = get_lcd_text()
        if lcd_txt != "":
            print(f"LCD TEXT: {lcd_txt}")
            callback(lcd_txt, publish_event, settings, code)
            time.sleep(delay+1)
