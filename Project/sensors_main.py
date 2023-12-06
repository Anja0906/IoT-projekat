import sys
import threading

from components.dht import run_dht
from components.door_ultrasonic_sensor import run_dus
from components.membrane_switch import run_dms
from components.door_pir import run_dpir
from components.door_button_sensor import run_ds
from project_settings.settings import load_settings

def run_dht_threads(settings, threads, stop_event):
    run_dht(settings['RDHT1'], threads, stop_event, 'RDHT1')
    run_dht(settings['RDHT2'], threads, stop_event, 'RDHT2')
    run_dht(settings['RDHT3'], threads, stop_event, 'RDHT3')
    run_dht(settings['RDHT4'], threads, stop_event, 'RDHT4')
    run_dht(settings['GDHT'], threads, stop_event, 'GDHT')


def run_pir_threads(settings, threads, stop_event):
    run_dpir(settings['RPIR1'], threads, stop_event, 'RPIR1')
    run_dpir(settings['RPIR2'], threads, stop_event, 'RPIR2')
    run_dpir(settings['RPIR3'], threads, stop_event, 'RPIR3')
    run_dpir(settings['RPIR4'], threads, stop_event, 'RPIR4')
    run_dpir(settings['DPIR1'], threads, stop_event, 'DPIR1')
    run_dpir(settings['DPIR2'], threads, stop_event, 'DPIR2')


def run_dus_threads(settings, threads, stop_event):
    run_dus(settings['DUS1'], threads, stop_event, 'DUS1')
    run_dus(settings['DUS2'], threads, stop_event, 'DUS2')


def run_dms_threads(settings, threads, stop_event):
    run_dms(settings['DMS'], threads, stop_event, 'DMS')


def run_ds_threads(settings, threads, stop_event):
    run_ds(settings['DS1'], threads, stop_event, 'DS1')
    run_ds(settings['DS2'], threads, stop_event, 'DS2')


def run_all_threads(settings, threads, stop_event):
    run_dht_threads(settings, threads, stop_event)
    run_pir_threads(settings, threads, stop_event)
    run_dus_threads(settings, threads, stop_event)
    run_dms_threads(settings, threads, stop_event)
    run_ds_threads(settings, threads, stop_event)
    for thread in threads:
        thread.join()


if __name__ == "__main__":
    settings = load_settings()
    threads = []
    stop_event = threading.Event()

    try:
        while True:
            run_all_threads(settings, threads, stop_event)
            stop_event.clear()
            threads = []

    except KeyboardInterrupt:
        print('Stopping app')
        for t in threads:
            stop_event.set()
        sys.exit(0)
