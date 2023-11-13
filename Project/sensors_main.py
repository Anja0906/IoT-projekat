import sys
import threading
import time
from components.dht import run_dht
from components.door_ultrasonic_sensor import run_dus
from components.membrane_switch import run_dms
from components.door_pir import run_dpir
from project_settings.settings import load_settings
from threading import Lock
print_lock = Lock()


def run_dht_threads(settings, threads, stop_event, print_lock):
    rdht1_settings = settings['RDHT1']
    rdht2_settings = settings['RDHT2']
    run_dht(rdht1_settings, threads, stop_event, 'RDHT1', print_lock)
    run_dht(rdht2_settings, threads, stop_event, 'RDHT2', print_lock)


def run_pir_threads(settings, threads, stop_event, print_lock):
    rpir1_settings = settings['RPIR1']
    rpir2_settings = settings['RPIR2']
    run_dpir(rpir1_settings, threads, stop_event, 'RPIR1', print_lock)
    run_dpir(rpir2_settings, threads, stop_event, 'RPIR2', print_lock)


def run_dpir_threads(settings, threads, stop_event, print_lock):
    dpir1_settings = settings['DPIR1']
    run_dpir(dpir1_settings, threads, stop_event, 'DPIR1', print_lock)


def run_dus_threads(settings, threads, stop_event, print_lock):
    dus1_settings = settings['DUS1']
    run_dus(dus1_settings, threads, stop_event, 'DUS1', print_lock)


def run_dms_threads(settings, threads, stop_event, print_lock):
    dms_settings = settings['DMS']
    run_dms(dms_settings, threads, stop_event, 'DMS', print_lock)


def run_all_threads(settings, threads, stop_event, print_lock):
    run_dht_threads(settings, threads, stop_event, print_lock)
    run_pir_threads(settings, threads, stop_event, print_lock)
    run_dpir_threads(settings, threads, stop_event, print_lock)
    run_dus_threads(settings, threads, stop_event, print_lock)
    run_dms_threads(settings, threads, stop_event, print_lock)
    for thread in threads:
        thread.join()


def start_your_sensors_daytona_500():
    print("Alright alright alright")
    time.sleep(1)
    print("Gentlemaaaaaaaaan")
    time.sleep(1)
    print("START")
    time.sleep(1)
    print("YOUR")
    time.sleep(1)
    print("SENSOOOOOOOOOORS")


if __name__ == "__main__":
    start_your_sensors_daytona_500()
    settings = load_settings()
    threads = []
    stop_event = threading.Event()

    try:
        while True:
            run_all_threads(settings, threads, stop_event, print_lock)
            stop_event.clear()
            threads = []

    except KeyboardInterrupt:
        print('Stopping app')
        for t in threads:
            stop_event.set()
        sys.exit(0)
