def motion_detected(channel, delay, callback, stop_event, publish_event, settings, code):
    print("You moved")
    callback(True, code, publish_event, settings)


def run_motion(pin, delay, callback, stop_event, publish_event, settings, code):
    from RPi.GPIO import GPIO
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(pin, GPIO.IN)
    GPIO.add_event_detect(pin, GPIO.RISING, callback=motion_detected, args=(delay, callback, stop_event, publish_event, settings, code))
    input("Press any key to exit...")
