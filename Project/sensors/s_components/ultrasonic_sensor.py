import RPi.GPIO as GPIO
import time


def get_distance(trigger_pin, echo_pin, code):
    GPIO.setmode(GPIO.BCM)
    TRIG_PIN = int(trigger_pin)
    ECHO_PIN = int(echo_pin)
    GPIO.setup(TRIG_PIN, GPIO.OUT)
    GPIO.setup(ECHO_PIN, GPIO.IN)
    GPIO.output(TRIG_PIN, False)
    time.sleep(0.2)
    GPIO.output(TRIG_PIN, True)
    time.sleep(0.00001)
    GPIO.output(TRIG_PIN, False)
    pulse_start_time = time.time()
    pulse_end_time = time.time()

    max_iter = 100

    iter = 0
    while GPIO.input(ECHO_PIN) == 0:
        if iter > max_iter:
            return None
        pulse_start_time = time.time()
        iter += 1

    iter = 0
    while GPIO.input(ECHO_PIN) == 1:
        if iter > max_iter:
            return None
        pulse_end_time = time.time()
        iter += 1

    pulse_duration = pulse_end_time - pulse_start_time
    distance = (pulse_duration * 34300) / 2
    return distance


def run_uds(trigger_pin, echo_pin, code):
    try:
        while True:
            distance = get_distance(trigger_pin, echo_pin, code)
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
