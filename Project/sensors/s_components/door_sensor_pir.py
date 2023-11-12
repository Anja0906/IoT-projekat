def motion_detected(channel):
    print("You moved")


def run_motion(pin,code):
    from RPi.GPIO import GPIO
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(pin, GPIO.IN)
    GPIO.add_event_detect(pin, GPIO.RISING, callback=motion_detected)
    input("Press any key to exit...")
