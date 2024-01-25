import time

def buzz_simulation(pin, pitch, duration, callback, publish_event, settings, code, stop_event):
    period = 1.0 / pitch
    delay = period / 2

    while True:
        if stop_event.is_set():
            print("EVO MEEEEE BZZZZZZZZ")
            for i in range(int(duration * pitch)):
                print(f"Pin {pin} ON")
                callback(publish_event, settings, code)
                time.sleep(delay)

                print(f"Pin {pin} OFF")
                callback(publish_event, settings, code)
                time.sleep(delay)

            time.sleep(1)

