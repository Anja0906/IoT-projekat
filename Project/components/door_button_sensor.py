import threading
import time

from sensors.s_simulators.door_sensor import run_ds_simulator


def ds_callback(current_value, code, print_lock):
    with print_lock:
        t = time.localtime()
        print("=" * 20)
        print(f"Timestamp: {time.strftime('%H:%M:%S', t)}")
        print(f"Code: {code}")
        if current_value:
            print(f"Door opened\n")
        else:
            print(f"Door closed\n")


def run_ds(settings, threads, stop_event, code, print_lock):
    if settings['simulated']:
        print("Starting " + code + " simulator")
        ds_thread = threading.Thread(target=run_ds_simulator, args=(5, ds_callback, stop_event, code, print_lock))
        ds_thread.start()
        threads.append(ds_thread)
        print(code + " simulator started\n")
    else:
        from sensors.s_components.door_sensor_button import press_button
        print("Starting " + code + " loop")
        pin = settings['pin']
        ds_thread = threading.Thread(target=press_button, args=(pin, code))
        ds_thread.start()
        threads.append(ds_thread)
        print(code + " loop started")
