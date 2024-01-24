import time

def run_display_simulator(delay, callback, alarm_event, publish_event, settings, code):
    while True:
        current_time = time.strftime("%H%M")
        callback(current_time, publish_event, settings, code)
        if alarm_event.is_set():
            time.sleep(0.5)
        else:
            time.sleep(delay)