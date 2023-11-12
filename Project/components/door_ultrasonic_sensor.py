import threading
import time
from sensors.s_simulators.ultrasonic_sensor import run_uds_simulator


def dus_callback(distance, code, print_lock):
    with print_lock:
        t = time.localtime()
        print("=" * 20)
        print(f"Timestamp: {time.strftime('%H:%M:%S', t)}")
        print(f"Code: {code}")
        print(f"Distance: " + str(distance) + " cm")


def run_dus(settings, threads, stop_event, code, print_lock):
    if settings['simulated']:
        print("Starting " + code + " simulator")
        dus_thread = threading.Thread(target=run_uds_simulator, args=(5, dus_callback, stop_event, code, print_lock))
        dus_thread.start()
        threads.append(dus_thread)
        print(code + " simulator started\n")
    else:
        from sensors.s_components.ultrasonic_sensor import get_distance
        print("Starting " + code + " loop")
        pin_trig = settings['pin_trig']
        pin_echo = settings['pin_echo']
        dus_thread = threading.Thread(target=get_distance, args=(pin_trig, pin_echo, code))
        dus_thread.start()
        threads.append(dus_thread)
        print(code + " loop started")
