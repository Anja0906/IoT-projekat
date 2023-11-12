import time


def buzz(pin, pitch, duration):
    import RPi.GPIO as GPIO
    pin = int(pin)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(pin, GPIO.OUT)
    period = 1.0 / pitch
    delay = period / 2
    cycles = int(duration * pitch)
    for i in range(cycles):
        GPIO.output(pin, True)
        time.sleep(delay)
        GPIO.output(pin, False)
        time.sleep(delay)
    time.sleep(1)