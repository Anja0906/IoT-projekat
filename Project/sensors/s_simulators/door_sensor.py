import time

from server.querry_service import query_ds_sensor


def run_ds_simulator(delay, callback, stop_event, publish_event, settings, code):
    while True:
        stop_event.wait()
        callback(stop_event, 1, publish_event, settings, code)
        if query_ds_sensor(code):
            print(f"Alarm: dugme {code} je pritisnuto duže od 5 sekundi")
        time.sleep(delay)
        stop_event.clear()