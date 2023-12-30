import sys
import threading

from components.buzzer_component import run_db
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


def run_pi1(settings, threads, stop_event):
    pir1_motion_detected_event = threading.Event()

    run_ds(settings['DS1'], threads, stop_event, 'DS1')
    run_dl(settings["DL"], threads, pir1_motion_detected_event, "DL")
    run_dus(settings['DUS1'], threads, pir1_motion_detected_event, 'DUS1')
    run_db(settings['DB'], threads, stop_event, 'DB')
    run_dpir(settings['DPIR1'], threads, pir1_motion_detected_event, 'DPIR1')
    run_dms(settings['DMS'], threads, stop_event, 'DMS')
    run_dpir(settings['RPIR1'], threads, stop_event, 'RPIR1')
    run_dpir(settings['RPIR2'], threads, stop_event, 'RPIR2')
    run_dht(settings['RDHT1'], threads, stop_event, 'RDHT1')
    run_dht(settings['RDHT2'], threads, stop_event, 'RDHT2')


def run_pi2(settings, threads, stop_event):
    run_ds(settings['DS2'], threads, stop_event, 'DS2')
    run_dus(settings['DUS2'], threads, stop_event, 'DUS2')
    run_dpir(settings['DPIR2'], threads, stop_event, 'DPIR2')
    run_dht(settings['GDHT'], threads, stop_event, 'GDHT')
    run_lcd(settings['GLCD'], threads, stop_event, 'GLCD')
    run_gyro(settings['GSG'], threads, stop_event, 'GSG')
    run_dpir(settings['RPIR3'], threads, stop_event, 'RPIR3')
    run_dht(settings['RDHT3'], threads, stop_event, 'RDHT3')


def run_pi3(settings, threads, stop_event):
    run_dpir(settings['RPIR4'], threads, stop_event, 'RPIR4')
    run_dht(settings['RDHT4'], threads, stop_event, 'RDHT4')
    run_db(settings['BB'], threads, stop_event, 'BB')
    run_clock(settings['B4SD'], threads, stop_event, 'B4SD')
    run_ir_receiver(settings['BIR'], threads, stop_event, 'BIR')
    run_rgb_light(settings['BRGB'], threads, stop_event, 'BRGB')


def run_all_threads(settings, threads, stop_event):
    run_pi1(settings, threads, stop_event)
    run_pi2(settings, threads, stop_event)
    run_pi3(settings, threads, stop_event)

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
