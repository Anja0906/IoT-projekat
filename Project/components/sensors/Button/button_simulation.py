import time

def run_ds_simulator(delay, callback, stop_event, publish_event, settings, code, client):
    while True:
        stop_event.wait()
        callback(stop_event, 1, publish_event, settings, code)
        time.sleep(delay)
        stop_event.clear()