import random
import time


def get_distance():
    return random.uniform(0.0, 200.0)


def generate_values():
    try:
        while True:
            distance = get_distance()
            yield distance
    except KeyboardInterrupt:
        print('Measurement stopped by user')
    except Exception as e:
        print(f'Error: {str(e)}')


def run_uds_simulator(delay, callback, stop_event, publish_event, settings):
    for distance in generate_values():
        time.sleep(delay) 
        callback(distance, publish_event, settings)
        if stop_event.is_set():
            break
