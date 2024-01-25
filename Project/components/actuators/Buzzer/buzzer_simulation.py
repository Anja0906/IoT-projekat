import time

def buzz_simulation(pin, pitch, duration, callback, publish_event, settings, code, stop_event, budilnik_event):
    period = 1.0 / pitch
    delay = period / 2

    while True:
        if stop_event.is_set() or budilnik_event.is_set():
            if(budilnik_event.is_set() and code == "BB"):
                print("BUDI SEEEE")
            for i in range(int(duration * pitch)):
                print(f"Pin {pin} ON")
                callback(publish_event, settings, code)
                time.sleep(delay)

                print(f"Pin {pin} OFF")
                callback(publish_event, settings, code)
                time.sleep(delay)

            time.sleep(1)

