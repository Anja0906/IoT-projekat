import RPi.GPIO as GPIO
from time import sleep

# disable warnings (optional)
GPIO.setwarnings(False)

GPIO.setmode(GPIO.BCM)

RED_PIN = 12
GREEN_PIN = 13
BLUE_PIN = 19

# set pins as outputs
GPIO.setup(RED_PIN, GPIO.OUT)
GPIO.setup(GREEN_PIN, GPIO.OUT)
GPIO.setup(BLUE_PIN, GPIO.OUT)


def turnOff(callback, stop_event, publish_event, settings, code):
    GPIO.output(RED_PIN, GPIO.LOW)
    GPIO.output(GREEN_PIN, GPIO.LOW)
    GPIO.output(BLUE_PIN, GPIO.LOW)
    callback("Off", publish_event, settings, code)


def white(callback, stop_event, publish_event, settings, code):
    GPIO.output(RED_PIN, GPIO.HIGH)
    GPIO.output(GREEN_PIN, GPIO.HIGH)
    GPIO.output(BLUE_PIN, GPIO.HIGH)
    callback("White", publish_event, settings, code)


def red(callback, stop_event, publish_event, settings, code):
    GPIO.output(RED_PIN, GPIO.HIGH)
    GPIO.output(GREEN_PIN, GPIO.LOW)
    GPIO.output(BLUE_PIN, GPIO.LOW)
    callback("Red", publish_event, settings, code)


def green(callback, stop_event, publish_event, settings, code):
    GPIO.output(RED_PIN, GPIO.LOW)
    GPIO.output(GREEN_PIN, GPIO.HIGH)
    GPIO.output(BLUE_PIN, GPIO.LOW)
    callback("Green", publish_event, settings, code)


def blue(callback, stop_event, publish_event, settings, code):
    GPIO.output(RED_PIN, GPIO.LOW)
    GPIO.output(GREEN_PIN, GPIO.LOW)
    GPIO.output(BLUE_PIN, GPIO.HIGH)
    callback("Blue", publish_event, settings, code)


def yellow(callback, stop_event, publish_event, settings, code):
    GPIO.output(RED_PIN, GPIO.HIGH)
    GPIO.output(GREEN_PIN, GPIO.HIGH)
    GPIO.output(BLUE_PIN, GPIO.LOW)
    callback("Yellow", publish_event, settings, code)


def purple(callback, stop_event, publish_event, settings, code):
    GPIO.output(RED_PIN, GPIO.HIGH)
    GPIO.output(GREEN_PIN, GPIO.LOW)
    GPIO.output(BLUE_PIN, GPIO.HIGH)
    callback("Purple", publish_event, settings, code)


def lightBlue(callback, stop_event, publish_event, settings, code):
    GPIO.output(RED_PIN, GPIO.LOW)
    GPIO.output(GREEN_PIN, GPIO.HIGH)
    GPIO.output(BLUE_PIN, GPIO.HIGH)
    callback("Light Blue", publish_event, settings, code)


def run_rgb_dioda(delay, callback, stop_event, publish_event, settings, code, client):
    try:
        while True:
            turnOff(callback, stop_event, publish_event, settings, code)
            sleep(delay)
            white(callback, stop_event, publish_event, settings, code)
            sleep(delay)
            red(callback, stop_event, publish_event, settings, code)
            sleep(delay)
            green(callback, stop_event, publish_event, settings, code)
            sleep(delay)
            blue(callback, stop_event, publish_event, settings, code)
            sleep(delay)
            yellow(callback, stop_event, publish_event, settings, code)
            sleep(delay)
            purple(callback, stop_event, publish_event, settings, code)
            sleep(delay)
            lightBlue(callback, stop_event, publish_event, settings, code)
            sleep(delay)
    except KeyboardInterrupt:
        GPIO.cleanup()
    except Exception as e:
        print(f'Error: {str(e)}')


