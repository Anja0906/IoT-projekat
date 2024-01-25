import time

def buzz(pin, pitch, duration, callback, publish_event, settings, code, stop_event):
    import RPi.GPIO as GPIO
    pin = int(pin)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(pin, GPIO.OUT)
    period = 1.0 / pitch
    delay = period / 2

    while True:
        if stop_event.is_set():
            for i in range(int(duration * pitch)):
                GPIO.output(pin, True)
                callback(publish_event, settings, code)
                time.sleep(delay)
                GPIO.output(pin, False)
                callback(publish_event, settings, code)
                time.sleep(delay)

            time.sleep(1)

    # GPIO.cleanup()