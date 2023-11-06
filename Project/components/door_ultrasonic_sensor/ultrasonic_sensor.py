import time
import random
import threading


class UltrasonicSensor(object):
    def __init__(self, trigger_pin, echo_pin, simulated):
        self.trigger_pin = trigger_pin,
        self.echo_pin = echo_pin,
        self.simulated = simulated

    def get_distance(self):
        if self.simulated:
            return random.uniform(0.0, 200.0)
        else:
            GPIO.output(self.trigger_pin, False)
            time.sleep(0.2)
            GPIO.output(self.trigger_pin, True)
            time.sleep(0.00001)
            GPIO.output(self.trigger_pin, False)
            pulse_start_time = time.time()
            pulse_end_time = time.time()

            max_iter = 100

            iterations = 0
            while GPIO.input(self.echo_pin) == 0:
                if iterations > max_iter:
                    return None
                pulse_start_time = time.time()
                iterations += 1

            iterations = 0
            while GPIO.input(self.echo_pin) == 1:
                if iterations > max_iter:
                    return None
                pulse_end_time = time.time()
                iterations += 1

            pulse_duration = pulse_end_time - pulse_start_time
            distance = (pulse_duration * 34300) / 2
            return distance

    def run_dioda_loop(self):
        from RPi.GPIO import GPIO
        GPIO.setup(self.trigger_pin, GPIO.OUT)
        GPIO.setup(self.echo_pin, GPIO.IN)
        try:
            while True:
                distance = self.get_distance()
                if distance is not None:
                    print(f'Distance: {distance} cm')
                else:
                    print('Measurement timed out')
                time.sleep(1)
        except KeyboardInterrupt:
            GPIO.cleanup()
            print('Measurement stopped by user')
        except Exception as e:
            print(f'Error: {str(e)}')

    def generate_values(self):
        try:
            while True:
                distance = self.get_distance()
                if distance is not None:
                    print(f'Distance: {round(distance, 2)} cm')
                else:
                    print('Measurement timed out')
                time.sleep(1)
        except KeyboardInterrupt:
            print('Measurement stopped by user')
        except Exception as e:
            print(f'Error: {str(e)}')

    def run(self, threads):
        stop_event = threading.Event()
        try:
            if self.simulated:
                print("Starting ultrasonic sensor simulator")
                uds_thread = threading.Thread(target=self.generate_values)
                uds_thread.start()
                threads.append(uds_thread)
            elif not self.simulated:
                print("Starting ultrasonic sensor loop")
                uds_thread = threading.Thread(target=self.run_dioda_loop)
                uds_thread.start()
                threads.append(uds_thread)
            else:
                print("Self.simulated is none")
        except KeyboardInterrupt:
            for t in threads:
                stop_event.set()
