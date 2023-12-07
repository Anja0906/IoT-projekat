import threading
import time

from sensors.s_components.lcd.LCD1602 import lcd_run
from sensors.s_simulators.lcd import simulate_lcd_display

result = True


def lcd_callback():
    global result
    t = time.localtime()
    print("=" * 20)
    print(f"Timestamp: {time.strftime('%H:%M:%S', t)}")


def run_lcd(settings, threads, stop_event, code):
    if settings['simulated']:
        lcd_thread = threading.Thread(target=simulate_lcd_display, args=(1, stop_event))
        lcd_thread.start()
        threads.append(lcd_thread)
    else:
        pin = settings['pin']
        dms_thread = threading.Thread(target=lcd_run(), args=())
        dms_thread.start()
        threads.append(dms_thread)
