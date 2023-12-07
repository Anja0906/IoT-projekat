import threading
import time
import random



def lcd_callback():
    global result
    t = time.localtime()
    print("=" * 20)
    print(f"Timestamp: {time.strftime('%H:%M:%S', t)}")


def run_lcd(settings, threads, stop_event):
    if settings['simulated']:
        from sensors.s_simulators.lcd_clock import run_display_simulator
        lcd_thread = threading.Thread(target=run_display_simulator, args=(1,lcd_callback()))
        lcd_thread.start()
        threads.append(lcd_thread)
    else:
        pin = settings['pin']
        # Dodajte logiku za upravljanje stvarnim LCD ekranom sa pin-om ovde
        pass

# Primer upotrebe
stop_event = threading.Event()
try:
    run_lcd({'simulated': True, 'pin': 17}, [], stop_event)
except KeyboardInterrupt:
    stop_event.set()
    print("Simulacija zaustavljena.")
