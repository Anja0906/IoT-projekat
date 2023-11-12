import threading
import time

from sensors.s_simulators.pir import run_pir_simulator


def dpir_callback(motion_detected, code):
    if motion_detected:
        t = time.localtime()
        print("=" * 20)
        print(f"Timestamp: {time.strftime('%H:%M:%S', t)}")
        print(f"Code: {code}")
        print(f"Motion detected\n")


def run_dpir(settings, threads, stop_event, code):
    if settings['simulated']:
        dpir_thread = threading.Thread(target=run_pir_simulator, args=(5, dpir_callback, stop_event, code))
        dpir_thread.start()
        threads.append(dpir_thread)
    else:
        from sensors.s_components.door_sensor_pir import motion_detected
        print("Starting " + code + " loop")
        pin = settings['pin']
        pir_thread = threading.Thread(target=motion_detected, args=(pin, code))
        pir_thread.start()
        threads.append(pir_thread)
        print(code + " loop started")
