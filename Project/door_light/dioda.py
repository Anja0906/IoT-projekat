import time
import random
import threading


class Dioda(object):
    def __init__(self, pin, simulated):
        self.pin = pin
        self.simulated = simulated

    def run_dioda_loop(self):
        try:
            from RPi.GPIO import GPIO
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

    @staticmethod
    def generate_values():
        try:
            while True:
                rnd = random.randint(0, 1)
                if rnd == 1:
                    print("Led is on")
                else:
                    print("Led is off")
                time.sleep(1)
        except KeyboardInterrupt:
            exit()

    def run(self, threads):
        if self.simulated:
            print("Starting dioda simulator")
            dioda_thread = threading.Thread(target=self.generate_values)
            dioda_thread.start()
            threads.append(dioda_thread)
            print("Dioda simulator started")
        elif not self.simulated:
            print("Starting dioda loop")
            dioda_thread = threading.Thread(target=self.run_dioda_loop)
            dioda_thread.start()
            threads.append(dioda_thread)
            print("Dioda loop started")
        else:
            print("Self.simulated is none")
