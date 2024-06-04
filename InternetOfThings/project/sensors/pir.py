import RPi.GPIO as GPIO

class PIR:
    def __init__(self, pin, name):
        self.pin = int(pin)
        self.name = name
        GPIO.setup(pin, GPIO.IN)


def motion_callback(channel, motion_detected, publish_event, settings):
    motion_detected(publish_event, settings, 1)


def run_pir_loop(pir, motion_detected, stop_event, publish_event, settings):
    def callback_wrapper(channel):
        motion_callback(channel, motion_detected, publish_event, settings)
    
    GPIO.add_event_detect(pir.pin, GPIO.RISING, callback=callback_wrapper)
    
    while True:
        if stop_event.is_set():
            GPIO.remove_event_detect(pir.pin)
            break
