import threading
import time

from components.buzzer_component import run_db
from components.dht import run_dht
from components.dioda import run_dl
from components.door_button_sensor import run_ds
from components.door_pir import run_dpir
from components.door_ultrasonic_sensor import run_dus
from components.membrane_switch import run_dms
from components.door_pir import run_dpir
from project_settings.settings import load_settings


def run_dht_threads(settings, threads, stop_event):
    rdht1_settings = settings['RDHT1']
    rdht2_settings = settings['RDHT2']
    run_dht(rdht1_settings, threads, stop_event, 'RDHT1')
    run_dht(rdht2_settings, threads, stop_event, 'RDHT2')


def run_pir_threads(settings, threads, stop_event):
    rpir1_settings = settings['RPIR1']
    rpir2_settings = settings['RPIR2']
    run_dpir(rpir1_settings, threads, stop_event, 'RPIR1')
    run_dpir(rpir2_settings, threads, stop_event, 'RPIR2')


def run_dpir_threads(settings, threads, stop_event):
    dpir1_settings = settings['DPIR1']

    run_dpir(dpir1_settings, threads, stop_event, 'DPIR1')


def run_ds_threads(settings, threads, stop_event):
    ds1_settings = settings['DS1']

    run_ds(ds1_settings, threads, stop_event, 'DS1')


def run_dus_threads(settings, threads, stop_event):
    dus1_settings = settings['DUS1']
    run_dus(dus1_settings, threads, stop_event, 'DUS1')


def run_dms_threads(settings, threads, stop_event):
    dms_settings = settings['DMS']
    run_dms(dms_settings, threads, stop_event, 'DMS')


def run_dl_threads(settings, threads, stop_event):
    dl_settings = settings["DL"]
    run_dl(dl_settings, threads, stop_event, "DL")


def run_db_threads(settings, threads, stop_event):
    db_settings = settings["DB"]
    run_db(db_settings, threads, stop_event, "DB")


def start_your_sensors_daytona_500():
    print("Alright alright alright")
    time.sleep(1)
    print("Gentlemaaaaaaaaan")
    time.sleep(1)
    print("START")
    time.sleep(1)
    print("YOUR")
    time.sleep(1)
    print("SENSOOOOOOOOOOOOOOOORS")


def display_menu():
    print("Menu Options:")
    print("Press l to control Door Light")
    print("Press b to control Door Buzzer")
    print("Press 'e' to exit the menu")


def process_menu_choice(choice, settings, threads, stop_event):
    if choice == "l":
        run_dl_threads(settings, threads, stop_event)
    elif choice == "b":
        run_db_threads(settings, threads, stop_event)
    elif choice == "x":
        print("Exiting the menu. Printing is resumed.")


def menu(stop_event):
    while not stop_event.is_set():
        user_input = input("Press 'm' to open the menu: ")
        if user_input == "m":
            display_menu()
            user_input = input("Enter your choice: ")
            process_menu_choice(user_input, settings, threads, stop_event)


def run_menu_thread(threads, stop_event):
    thread = threading.Thread(target=menu, args=(stop_event,))
    thread.start()
    threads.append(thread)


def run_all_threads(settings, threads, stop_event):
    run_dht_threads(settings, threads, stop_event)
    run_pir_threads(settings, threads, stop_event)
    run_dpir_threads(settings, threads, stop_event)
    run_dus_threads(settings, threads, stop_event)
    run_dms_threads(settings, threads, stop_event)
    run_dl_threads(settings, threads, stop_event)
    run_db_threads(settings, threads, stop_event)



if __name__ == "__main__":
    start_your_sensors_daytona_500()

    settings = load_settings()
    threads = []
    stop_event = threading.Event()

    try:
        while not stop_event.is_set():
            run_all_threads(settings, threads, stop_event)
            run_menu_thread(threads, stop_event)
            time.sleep(5)
    except KeyboardInterrupt:
        print('Stopping app')
        stop_event.set()

    print("App stopped")
