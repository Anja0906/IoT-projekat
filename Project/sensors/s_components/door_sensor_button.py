def press_button(pin, code):
    import RPi.GPIO as GPIO
    PORT_BUTTON = int(pin)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(PORT_BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.add_event_detect(PORT_BUTTON, GPIO.RISING, callback=pressed_button, bouncetime=100)
