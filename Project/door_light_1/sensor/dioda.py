import RPi.GPIO as GPIO
import time

class Dioda(object):

    def __init__(self, pin):
        self.pin = pin

    def run_dioda_loop(self):
        try:
            while True:
                GPIO.setmode(GPIO.BCM)
                GPIO.setup(self.pin, GPIO.OUT)
                print("LED on")
                GPIO.output(self.pin, GPIO.HIGH)
                time.sleep(1)
                print("LED off")
                GPIO.output(self.pin, GPIO.LOW)
        except KeyboardInterrupt:
            exit()



