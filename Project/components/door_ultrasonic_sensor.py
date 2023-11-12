import threading
import time
from sensors.s_simulators.ultrasonic_sensor import run_uds_simulator


def dus_callback(distance, code):
    t = time.localtime()
    print("=" * 20)
    print(f"Timestamp: {time.strftime('%H:%M:%S', t)}")
    print(f"Code: {code}")
    print(f"Distance: " + str(distance) + " cm")


def run_dus(settings, threads, stop_event, code):
    if settings['simulated']:
        print("Starting " + code + " sumilator")
        dus_thread = threading.Thread(target=run_uds_simulator, args=(5, dus_callback, stop_event, code))
        dus_thread.start()
        threads.append(dus_thread)
        print(code + " sumilator started\n")
    else:
        from sensors.s_components.ultrasonic_sensor import detect_distance
        print("Starting " + code + " loop")
        pin_trig = settings['pin_trig']
        pin_echo = settings['pin_echo']
        dus_thread = threading.Thread(target=detect_distance, args=(pin_trig, pin_echo, code))
        dus_thread.start()
        threads.append(dus_thread)
        print(code + " loop started")
