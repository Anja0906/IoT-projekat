import time
import random


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


def run_uds_simulator(delay, callback, stop_event, publish_event, settings, code):
    generator = generate_values()
    while True:
        stop_event.wait()
        g = next(generator)
        print(f"Generated distance: {g}")  # Logovanje generisane udaljenosti
        time.sleep(delay)
        callback(g, publish_event, settings)
        stop_event.clear()




