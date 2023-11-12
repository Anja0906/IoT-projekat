import threading
import time

result = True


def dl_callback():
    global result
    t = time.localtime()
    print("=" * 20)
    print(f"Timestamp: {time.strftime('%H:%M:%S', t)}")
    if result:
        result = False
        print("Light is on\n")
    else:
        result = True
        print("Light is off\n")


def run_dl(settings, threads, stop_event, code):
    if settings['simulated']:
        dl_thread = threading.Thread(target=dl_callback, args=())
        dl_thread.start()
        threads.append(dl_thread)
    else:
        pin = settings['pin']
        from actuators.dioda import run_dl
        dms_thread = threading.Thread(target=run_dl, args=(pin, code))
        dms_thread.start()
        threads.append(dms_thread)

