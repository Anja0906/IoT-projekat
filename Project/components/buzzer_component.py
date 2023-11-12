import threading
import time

from actuators.buzzer import buzz


def db_callback():
    t = time.localtime()
    print("="*20)
    print(f"Timestamp: {time.strftime('%H:%M:%S', t)}")
    print("Buzzzing\n")


def run_db(settings, threads, stop_event, code):
        if settings['simulated']:
            db_thread = threading.Thread(target=db_callback, args=())
            db_thread.start()
            threads.append(db_thread)
        else:
            pin =settings['pin']
            db_thread = threading.Thread(target=buzz, args=(pin))
            db_thread.start()
            threads.append(db_thread)