import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

segments = (11, 4, 23, 8, 7, 10, 18, 25)
digits = (22, 27, 17, 24)

num = {' ': (0, 0, 0, 0, 0, 0, 0),
       '0': (1, 1, 1, 1, 1, 1, 0),
       '1': (0, 1, 1, 0, 0, 0, 0),
       '2': (1, 1, 0, 1, 1, 0, 1),
       '3': (1, 1, 1, 1, 0, 0, 1),
       '4': (0, 1, 1, 0, 0, 1, 1),
       '5': (1, 0, 1, 1, 0, 1, 1),
       '6': (1, 0, 1, 1, 1, 1, 1),
       '7': (1, 1, 1, 0, 0, 0, 0),
       '8': (1, 1, 1, 1, 1, 1, 1),
       '9': (1, 1, 1, 1, 0, 1, 1)}

for segment in segments:
    GPIO.setup(segment, GPIO.OUT)
    GPIO.output(segment, 0)

for digit in digits:
    GPIO.setup(digit, GPIO.OUT)
    GPIO.output(digit, 1)


def run_clock(delay, callback, alarm_event, publish_event, settings, code):
    try:
        while True:
            n = time.ctime()[11:13] + time.ctime()[14:16]
            s = str(n).rjust(4)

            for digit in range(4):
                for loop in range(0, 7):
                    GPIO.output(segments[loop], num[s[digit]][loop])
                GPIO.output(digits[digit], 0)
                time.sleep(0.001)
                GPIO.output(digits[digit], 1)

            if alarm_event.is_set():
                for digit in digits:
                    GPIO.output(digit, 0)
                time.sleep(0.5)

                for digit in digits:
                    GPIO.output(digit, 1)
                time.sleep(0.5)

            callback(s, publish_event, settings, code)

    finally:
        GPIO.cleanup()