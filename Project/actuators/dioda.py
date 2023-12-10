import RPi.GPIO as GPIO
import time


def init_gpio(pin):
    pin = int(pin)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(pin, GPIO.OUT)


def run_dl(pin, callback, publish_event, settings, code):
    init_gpio(pin)
    print("Led On")
    GPIO.output(pin, GPIO.HIGH)
    callback(publish_event, settings, code)
    time.sleep(1)
    print("Led Of")
    GPIO.output(pin, GPIO.LOW)
    callback(publish_event, settings, code)
