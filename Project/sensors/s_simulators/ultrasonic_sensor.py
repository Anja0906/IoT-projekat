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


def run_uds_simulator(delay, callback, pir_motion_detected_event, publish_event, settings, read_from_db_event, code):
    generator = generate_values()
    while True:
        pir_motion_detected_event.wait()
        g = next(generator)
        print(f"Detected distance: {g} on {code}\n")
        time.sleep(delay)
        callback(g, publish_event, pir_motion_detected_event, settings, read_from_db_event)
        pir_motion_detected_event.clear()




