import RPi.GPIO as GPIO
import time


class Dioda:
    def __init__(self, name, pin):
        self.pin = int(pin)
        self.name = name
        self.is_on = False
        GPIO.setup(self.pin, GPIO.OUT)

    def switch_light(self):
        self.is_on = not self.is_on
        if self.is_on:
            GPIO.output(self.pin, GPIO.HIGH)
        else:
            GPIO.output(self.pin, GPIO.LOW)


def run_dioda_loop(pipe, dioda, delay, callback, stop_event, publish_event, settings):
    last_dioda_time = time.time()
    while True:
        if pipe.poll():
            message = pipe.recv()
            message = str(message).strip().lower()
            if message == "l":
                last_dioda_time = time.time()

        dioda.is_on = time.time() - last_dioda_time <= 10
        callback(dioda.is_on, publish_event, settings)
        if stop_event.is_set():
            break
        time.sleep(delay)
