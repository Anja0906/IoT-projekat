import time
import random


def get_distance():
    return random.uniform(0.0, 200.0)


def generate_values():
    try:
        while True:
            distance = get_distance()
            if distance is not None:
                print(f'Distance: {round(distance, 2)} cm')
            else:
                print('Measurement timed out')
            yield distance

    except KeyboardInterrupt:
        print('Measurement stopped by user')
    except Exception as e:
        print(f'Error: {str(e)}')


def run_uds_simulator(delay, callback, stop_event, publish_event, settings, code):
    for g in generate_values():
        time.sleep(delay)
        callback(g, publish_event, settings, code)
        if stop_event.is_set():
            break
