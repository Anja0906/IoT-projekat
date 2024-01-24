def pressed_button(pin, callback, stop_event, publish_event, settings, code):
    print("You moved")
    callback(1, publish_event, settings, code)
def press_button(pin, callback, stop_event, publish_event, settings, code):
    import RPi.GPIO as GPIO
    PORT_BUTTON = int(pin)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(PORT_BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.add_event_detect(PORT_BUTTON, GPIO.RISING, callback=pressed_button, args=(pin, callback, stop_event, publish_event, settings, code), bouncetime=100)
