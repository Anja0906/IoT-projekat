import sys
import threading
from components.dht import run_dht
from components.dioda import run_dl
from components.door_ultrasonic_sensor import run_dus
from components.gyro import run_gyro
from components.ir_receiver import run_ir_receiver
from components.lcd import run_lcd
from components.lcd_clock import run_clock
from components.membrane_switch import run_dms
from components.door_pir import run_dpir
from components.door_button_sensor import run_ds
from components.rgb_dioda import run_rgb_light
from project_settings.settings import load_settings

def run_dht_threads(settings, threads, stop_event):
    run_dht(settings['RDHT1'], threads, stop_event, 'RDHT1')
    run_dht(settings['RDHT2'], threads, stop_event, 'RDHT2')
    run_dht(settings['RDHT3'], threads, stop_event, 'RDHT3')
    run_dht(settings['RDHT4'], threads, stop_event, 'RDHT4')
    run_dht(settings['GDHT'], threads, stop_event, 'GDHT')


def run_pir_threads(settings, threads, stop_event):
    pir1_motion_detected_event = threading.Event()
    pir2_motion_detected_event = threading.Event()
    read_from_db_event_dus1 = threading.Event()
    read_from_db_event_dus2 = threading.Event()
    run_dpir(settings['RPIR1'], threads, stop_event, 'RPIR1')
    run_dpir(settings['RPIR2'], threads, stop_event, 'RPIR2')
    run_dpir(settings['RPIR3'], threads, stop_event, 'RPIR3')
    run_dpir(settings['RPIR4'], threads, stop_event, 'RPIR4')
    run_dpir(settings['DPIR1'], threads, pir1_motion_detected_event, 'DPIR1')
    run_dpir(settings['DPIR2'], threads, pir2_motion_detected_event, 'DPIR2')
    run_dl_threads(settings, threads, pir1_motion_detected_event)
    run_dus(settings['DUS1'], threads, pir1_motion_detected_event, read_from_db_event_dus1, 'DUS1')
    run_dus(settings['DUS2'], threads, pir2_motion_detected_event, read_from_db_event_dus2,'DUS2')

def run_dms_threads(settings, threads, stop_event):
    run_dms(settings['DMS'], threads, stop_event, 'DMS')


def run_ds_threads(settings, threads, stop_event):
    run_ds(settings['DS1'], threads, stop_event, 'DS1')
    run_ds(settings['DS2'], threads, stop_event, 'DS2')


def run_gyro_threads(settings, threads, stop_event):
    run_gyro(settings['GSG'], threads, stop_event, 'GSG')


def run_lcd_threads(settings, threads, stop_event):
    run_lcd(settings['GLCD'], threads, stop_event, 'GLCD')


def run_clock_threads(settings, threads, stop_event):
    run_clock(settings['B4SD'], threads, stop_event, 'B4SD')


def run_bir_and_dioda_threads(settings, threads):
    ir_changed_event = threading.Event()
    run_ir_receiver(settings['BIR'], threads, ir_changed_event, 'BIR')
    run_rgb_light(settings['BRGB'], threads, ir_changed_event, 'BRGB')


def run_dl_threads(settings, threads, stop_event):
    dl_settings = settings["DL"]
    run_dl(dl_settings, threads, stop_event, "DL")


def run_all_threads(settings, threads, stop_event):
    run_dht_threads(settings, threads, stop_event)
    run_pir_threads(settings, threads, stop_event)
    run_dms_threads(settings, threads, stop_event)
    run_ds_threads(settings, threads, stop_event)
    run_gyro_threads(settings, threads, stop_event)
    run_lcd_threads(settings, threads, stop_event)
    run_clock_threads(settings, threads, stop_event)
    run_bir_and_dioda_threads(settings, threads)

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
