import threading

import keyboard


class MembraneSwitch(object):
    def __init__(self, pin, simulated, opened=False):
        self.pin = pin
        self.simulated = simulated
        self.opened = opened

    def button_pressed(self, event):
        self.opened = not self.opened
        print("Switch is ON" if self.opened else "Switch is OFF")

    def run_switch_loop(self):
        from RPi.GPIO import GPIO
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(self.pin, GPIO.RISING, callback=self.button_pressed, bouncetime=100)

    def run_switch_simulation(self):
        keyboard.on_press_key("enter", self.button_pressed)
        try:
            while True:
                input("Press Enter to toggle the switch>>> ")

        except KeyboardInterrupt:
            pass
        finally:
            keyboard.unhook_all()

    def run(self, threads):
        stop_event = threading.Event()
        try:
            if self.simulated:
                print("Starting switch simulator")
                switch_thread = threading.Thread(target=self.run_switch_simulation)
                switch_thread.start()
                threads.append(switch_thread)
            elif not self.simulated:
                print("Starting switch loop")
                switch_thread = threading.Thread(target=self.run_switch_loop)
                switch_thread.start()
                threads.append(switch_thread)
            else:
                print("Self.simulated is none")
        except KeyboardInterrupt:
            for t in threads:
                stop_event.set()
