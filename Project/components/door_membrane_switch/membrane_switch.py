import threading
import time

import keyboard


class MembraneSwitch(object):
    def __init__(self, simulated, r1, r2, r3, r4, c1, c2, c3, c4):
        self.simulated = simulated

        self.R1 = r1
        self.R2 = r2
        self.R3 = r3
        self.R4 = r4

        self.C1 = c1
        self.C2 = c2
        self.C3 = c3
        self.C4 = c4

        self.pressed_keys = []
        if not self.simulated:
            self.init_gpio()

    def init_gpio(self):
        from RPi import GPIO
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)

        GPIO.setup(self.R1, GPIO.OUT)
        GPIO.setup(self.R2, GPIO.OUT)
        GPIO.setup(self.R3, GPIO.OUT)
        GPIO.setup(self.R4, GPIO.OUT)

        # Configure input pins to use the internal pull-down resistors
        GPIO.setup(self.C1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(self.C2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(self.C3, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(self.C4, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    def read_line(self, line, characters):
        GPIO.output(line, GPIO.HIGH)
        pressed_keys = []
        if GPIO.input(self.C1) == 1:
            pressed_keys.append(characters[0])
        if GPIO.input(self.C2) == 1:
            pressed_keys.append(characters[1])
        if GPIO.input(self.C3) == 1:
            pressed_keys.append(characters[2])
        if GPIO.input(self.C4) == 1:
            pressed_keys.append(characters[3])
        GPIO.output(line, GPIO.LOW)
        return pressed_keys

    def start_reading(self):
        try:
            while True:
                keys = self.read_line(self.R1, ["1", "2", "3", "A"])
                keys.extend(self.read_line(self.R2, ["4", "5", "6", "B"]))
                keys.extend(self.read_line(self.R3, ["7", "8", "9", "C"]))
                keys.extend(self.read_line(self.R4, ["*", "0", "#", "D"]))
                if keys:
                    self.pressed_keys = keys
                    print("Pressed keys:", keys)
                time.sleep(0.2)
        except KeyboardInterrupt:
            print("\nApplication stopped!")

    def on_key_event(self, event):
        if event.event_type == keyboard.KEY_DOWN:
            key = event.name
            self.pressed_keys.append(key)
            print(f"\nPressed key: {key}")

    def start_listening(self):
        keyboard.hook(self.on_key_event)

    def start_reading_simulation(self):
        self.start_listening()
        keyboard.wait("esc")

    def run(self, threads):
        stop_event = threading.Event()
        try:
            if self.simulated:
                print("Starting door membrane simulator")
                membrane_switch_thread = threading.Thread(target=self.start_reading_simulation)
                membrane_switch_thread.start()
                threads.append(membrane_switch_thread)
            elif not self.simulated:
                print("Starting dioda loop")
                membrane_switch_thread = threading.Thread(target=self.start_listening())
                membrane_switch_thread.start()
                threads.append(membrane_switch_thread)
            else:
                print("Self.simulated is none")
        except KeyboardInterrupt:
            for t in threads:
                stop_event.set()



