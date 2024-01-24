import threading
import time
from RPi import GPIO

def dioda_light_control(pin, callback, publish_event, settings, code, motion_detected_event):
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(pin, GPIO.OUT)

    def turn_off_light():
        print("LED Off")
        GPIO.output(pin, GPIO.LOW)
        callback(publish_event, settings, code, False)
        motion_detected_event.clear()

    timer = None
    while True:
        motion_detected_event.wait()

        if timer is not None:
            timer.cancel()

        print("LED On")
        GPIO.output(pin, GPIO.HIGH)
        callback(publish_event, settings, code, True)

        timer = threading.Timer(10, turn_off_light)
        timer.start()
        motion_detected_event.clear()

    GPIO.cleanup()


