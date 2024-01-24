import threading

def dioda_light_control(callback, publish_event, settings, motion_detected_event, code):
    timer = None
    def turn_off_light():
        nonlocal timer
        callback(publish_event, settings, code, False)
        print("UGASIO SAM")

    while True:
        motion_detected_event.wait()
        if timer is not None:
            timer.cancel()
        callback(publish_event, settings, code, True)
        timer = threading.Timer(10, turn_off_light)
        timer.start()
        motion_detected_event.clear()