import RPi.GPIO as GPIO
import time


class UDS:
    def __init__(self, trig_pin, echo_pin, name):
        self.trig_pin = trig_pin
        self.echo_pin = echo_pin
        GPIO.setup(self.trig_pin, GPIO.OUT)
        GPIO.setup(self.echo_pin, GPIO.IN)
        self.max_iter = 100
        self.name = name

    def get_distance(self):
        GPIO.output(self.trig_pin, False)
        time.sleep(0.2)
        GPIO.output(self.trig_pin, True)
        time.sleep(0.00001)
        GPIO.output(self.trig_pin, False)
        pulse_start_time = time.time()
        pulse_end_time = time.time()

        iter = 0
        while GPIO.input(self.echo_pin) == 0:
            if iter > self.max_iter:
                return None
            pulse_start_time = time.time()
            iter += 1

        iter = 0
        while GPIO.input(self.echo_pin) == 1:
            if iter > self.max_iter:
                return None
            pulse_end_time = time.time()
            iter += 1

        pulse_duration = pulse_end_time - pulse_start_time
        distance = (pulse_duration * 34300) / 2
        return distance


def run_uds_loop(uds, delay, callback, stop_event, publish_event, settings):
    try:
        while True:
            distance = uds.get_distance(trigger_pin, echo_pin)
            if distance is not None:
                callback(distance, publish_event, settings)
            else:
                print('Measurement timed out')
            time.sleep(delay)
    except KeyboardInterrupt:
        GPIO.cleanup()
        print('Measurement stopped by user')
    except Exception as e:
        print(f'Error: {str(e)}')
   
