import threading
import time

door_open = False


def ds_callback(code, print_lock):
    global door_open
    with print_lock:
        t = time.localtime()
        print("=" * 20)
        print(f"Timestamp: {time.strftime('%H:%M:%S', t)}")
        print(f"Code: {code}")
        if door_open:
            door_open = not door_open
            print("Door is currently opened")
        else:
            door_open = not door_open
            print("Door is currently closed")


def run_ds(settings, threads, stop_event, code, print_lock):
    if settings['simulated']:
        ds_thread = threading.Thread(target=ds_callback, args=(code, print_lock))
        ds_thread.start()
        threads.append(ds_thread)
    else:
        from sensors.s_components.door_sensor_button import press_button
        pin = settings['pin']
        ds_thread = threading.Thread(target=press_button, args=(pin, code))
        ds_thread.start()
        threads.append(ds_thread)
