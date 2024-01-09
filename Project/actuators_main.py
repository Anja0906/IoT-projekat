import threading
import time

from components.buzzer_component import run_db
from components.dioda import run_dl
from components.door_button_sensor import run_ds
from project_settings import settings
from project_settings.settings import load_settings

print_lock = threading.Lock()


def run_dl_threads(settings, threads, stop_event):
    dl_settings = settings["DL"]
    run_dl(dl_settings, threads, stop_event, "DL")


def run_db_threads(settings, threads, stop_event, choice):
    if choice == 1:
        run_db(settings["DB"], threads, stop_event, "DB")
    else:
        run_db(settings["BB"], threads, stop_event, "BB")


def run_menu_thread(threads, stop_event):
    thread = threading.Thread(target=menu, args=(stop_event,))
    thread.start()
    threads.append(thread)


def wait_for_button_press(stop_event, delay, char):
    while True:
        with print_lock:
            input_char = input(f"Pritisnite '{char}' i pritisnite enter za aktivaciju: ")
            if input_char and input_char[0].lower() == char:
                stop_event.set()
        time.sleep(delay)


def run_button_awaiter(stop_event, threads, char):
    awaiter_thread = threading.Thread(target=wait_for_button_press,
                                      args=(stop_event, 1, char))
    awaiter_thread.start()
    threads.append(awaiter_thread)


def run_ds_threads(settings, threads, stop_event):
    ds1_pressed_event = threading.Event()
    ds2_pressed_event = threading.Event()

    run_ds(settings['DS1'], threads, ds1_pressed_event, 'DS1')
    run_ds(settings['DS2'], threads, ds2_pressed_event, 'DS2')
    run_button_awaiter(ds1_pressed_event, threads, 'a')
    run_button_awaiter(ds2_pressed_event, threads, 'b')


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
        user_input = input("\nEnter your choice: ")
        process_menu_choice(user_input, settings, threads, stop_event)


if __name__ == "__main__":
    settings = load_settings()
    threads = []
    stop_event = threading.Event()

    # try:
    #     run_menu_thread(threads, stop_event)
    #     while not stop_event.is_set():
    #         time.sleep(5)
    # except KeyboardInterrupt:
    #     print('Stopping app')
    #     for t in threads:
    #         stop_event.set()
    #
    # print("App stopped")

    run_ds_threads(settings, threads, stop_event)
