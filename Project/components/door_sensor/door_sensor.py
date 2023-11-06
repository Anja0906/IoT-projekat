import time
import random
import threading


class MotionSensor(object):
    def __init__(self, pin, simulated):
        self.pin = pin
        self.simulated = simulated

    def motion_detected(self, channel):
        print("You moved")

    def no_motion(self, channel):
        print("You stopped moving")

    def run_motion(self):
        from RPi.GPIO import GPIO
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.IN)
        GPIO.add_event_detect(self.pin, GPIO.RISING, callback=self.motion_detected)
        input("Press any key to exit...")

    def run_simulation(self):
        while True:
            rnd = random.randint(0, 1)
            if rnd == 1:
                self.motion_detected(None)
            else:
                self.no_motion(None)
            time.sleep(1)

    def run(self, threads):
        stop_event = threading.Event()
        try:
            if self.simulated:
                print("Starting motion simulator")
                motion_thread = threading.Thread(target=self.run_simulation, args=())
                motion_thread.start()
                threads.append(motion_thread)
            elif not self.simulated:
                print("Starting motion loop")
                motion_thread = threading.Thread(target=self.run_motion, args=())
                motion_thread.start()
                threads.append(motion_thread)
            else:
                print("Self.simulated is none")
        except KeyboardInterrupt:
            for t in threads:
                stop_event.set()
