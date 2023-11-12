import threading
import time

from components.buzzer_component import run_db
from components.dioda import run_dl
from project_settings import settings
from project_settings.settings import load_settings


def run_dl_threads(settings, threads, stop_event):
    dl_settings = settings["DL"]
    run_dl(dl_settings, threads, stop_event, "DL")


def run_db_threads(settings, threads, stop_event):
    db_settings = settings["DB"]
    run_db(db_settings, threads, stop_event, "DB")


def run_menu_thread(threads, stop_event):
    thread = threading.Thread(target=menu, args=(stop_event,))
    thread.start()
    threads.append(thread)


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


def start_your_sensors_daytona_500():
    print("Alright alright alright")
    time.sleep(1)
    print("Gentlemaaaaaaaaan")
    time.sleep(1)
    print("START")
    time.sleep(1)
    print("YOUR")
    time.sleep(1)
    print("ACTUATOOOOOORS")


def menu(stop_event):
    while not stop_event.is_set():
        display_menu()
        user_input = input("Enter your choice: ")
        process_menu_choice(user_input, settings, threads, stop_event)


if __name__ == "__main__":
    start_your_sensors_daytona_500()
    settings = load_settings()
    threads = []
    stop_event = threading.Event()

    try:
        run_menu_thread(threads, stop_event)
        while not stop_event.is_set():
            time.sleep(5)
    except KeyboardInterrupt:
        print('Stopping app')
        for t in threads:
            stop_event.set()

    print("App stopped")
