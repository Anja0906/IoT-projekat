import time


def run_dioda_simulator(pipe, delay, callback, stop_event, publish_event, settings):
    last_dioda_time = time.time()
    while True:

        if pipe.poll():
            message = pipe.recv()
            message = str(message).strip().lower()
            if message == "l":
                last_dioda_time = time.time()

        dioda_state = time.time() - last_dioda_time <= 10

        time.sleep(delay)  
        callback(dioda_state, publish_event, settings)
        if stop_event.is_set():
            break