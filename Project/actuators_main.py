import threading
import time

from components.buzzer_component import run_db
from components.dioda import run_dl
from project_settings import settings
from project_settings.settings import load_settings

print_lock = threading.Lock()


def run_dl_threads(settings, threads, stop_event):
    dl_settings = settings["DL"]
    run_dl(dl_settings, threads, stop_event, "DL")


def run_db_threads(settings, threads, stop_event, choice):
    if choice==1:
        run_db(settings["DB"], threads, stop_event, "DB")
    else:
        run_db(settings["BB"], threads, stop_event, "BB")


def run_menu_thread(threads, stop_event):
    thread = threading.Thread(target=menu, args=(stop_event,))
    thread.start()
    threads.append(thread)


def display_menu():
    print("Menu Options:")
    print("Press l to control Door Light")
    print("Press b1 to control Door Buzzer")
    print("Press b2 to control Bedroom Buzzer")
    print("Press 'e' to exit the menu")


def process_menu_choice(choice, settings, threads, stop_event):
    if choice == "l":
        run_dl_threads(settings, threads, stop_event)
    elif choice == "b1":
        run_db_threads(settings, threads, stop_event, 1)
    elif choice == "b2":
        run_db_threads(settings, threads, stop_event, 2)
    elif choice == "x":
        print("Exiting the menu. Printing is resumed.")


def menu(stop_event):
    while not stop_event.is_set():
        display_menu()
        user_input = input("Enter your choice: ")
        process_menu_choice(user_input, settings, threads, stop_event)


if __name__ == "__main__":
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
