import sys
import threading
import time

from components.sensors.DHT.dht_component import run_dht
from components.actuators.Dioda.dioda_component import run_dl
from components.sensors.DUS.dus_component import run_dus
from components.sensors.Gyro.gyro_component import run_gyro
from components.sensors.IR.ir_component import run_ir_receiver
from components.sensors.LCD.lcd_component import run_lcd
from components.sensors.Clock.clock_component import run_clock
from components.sensors.MembraneSwitch.membrane_switch_component import run_dms
from components.sensors.PIR.pir_component import run_dpir
from components.sensors.Button.button_component import run_ds
from components.sensors.RGB_Dioda.rgb_component import run_rgb_light
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
    ds1_pressed_event = threading.Event()
    ds2_pressed_event = threading.Event()
    run_ds(settings['DS1'], threads, ds1_pressed_event, 'DS1')
    run_ds(settings['DS2'], threads, ds2_pressed_event, 'DS2')
    run_button_awaiter(ds1_pressed_event, threads, 'a')
    # run_button_awaiter(ds2_pressed_event, threads, 'b')


def run_gyro_threads(settings, threads, stop_event):
    run_gyro(settings['GSG'], threads, stop_event, 'GSG')


def run_lcd_threads(settings, threads, stop_event):
    run_lcd(settings['GLCD'], threads, stop_event, 'GLCD')


def wait_for_button_press(stop_event, delay, char):
    while True:
        input_char = input(f"Pritisnite '{char}' za aktivaciju: ")
        if input_char.lower() == char:
            stop_event.set()
        time.sleep(1)

def run_button_awaiter(stop_event, threads, char):
    awaiter_thread = threading.Thread(target=wait_for_button_press,
                                  args=(stop_event, 5, char))
    awaiter_thread.start()
    threads.append(awaiter_thread)

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
    # run_dht_threads(settings, threads, stop_event)
    # run_pir_threads(settings, threads, stop_event)
    # run_dms_threads(settings, threads, stop_event)
    # run_ds_threads(settings, threads, stop_event)
    # run_gyro_threads(settings, threads, stop_event)
    # run_lcd_threads(settings, threads, stop_event)
    # run_clock_threads(settings, threads, stop_event)
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
