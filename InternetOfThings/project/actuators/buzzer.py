import time
import RPi.GPIO as GPIO
from queue import Queue
from threading import Event, Thread

# Definicija frekvencija za note
NOTES = {
    'cL': 129, 'cLS': 139, 'dL': 146, 'dLS': 156, 'eL': 163, 'fL': 173,
    'fLS': 185, 'gL': 194, 'gLS': 207, 'aL': 219, 'aLS': 228, 'bL': 232,
    'c': 261, 'cS': 277, 'd': 294, 'dS': 311, 'e': 329, 'f': 349,
    'fS': 370, 'g': 391, 'gS': 415, 'a': 440, 'aS': 455, 'b': 466,
    'cH': 523, 'cHS': 554, 'dH': 587, 'dHS': 622, 'eH': 659, 'fH': 698,
    'fHS': 740, 'gH': 784, 'gHS': 830, 'aH': 880, 'aHS': 910, 'bH': 933
}

class Buzzer:
    def __init__(self, name, pin):
        self.name = name
        self.pin = pin
        self.interrupt = Queue()
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.OUT)
        
    def turn_on(self):
        GPIO.output(self.pin, GPIO.HIGH)
        
    def turn_off(self):
        GPIO.output(self.pin, GPIO.LOW)
        
    def is_buzzer_on(self):
        return GPIO.input(self.pin) == GPIO.HIGH

    def buzz(self, note, duration):
        if note not in NOTES:
            raise ValueError(f"Invalid note: {note}")
        pitch = NOTES[note]
        period = 1.0 / pitch
        delay = period / 2

        for _ in range(int(duration * pitch)):
            if not self.interrupt.empty() and self.interrupt.get():
                break
            GPIO.output(self.pin, GPIO.HIGH)
            time.sleep(delay)
            GPIO.output(self.pin, GPIO.LOW)
            time.sleep(delay)

        GPIO.output(self.pin, GPIO.LOW)
        time.sleep(0.02)

    def play(self, melody, durations):
        for note, duration in zip(melody, durations):
            if not self.interrupt.empty() and self.interrupt.get():
                self.turn_off()
                return
            self.buzz(note, duration / 1000.0)  # Convert ms to seconds
        time.sleep(0.25)

def run_db_loop(should_turn_on_db, should_turn_on_bb, input_queue, db, delay, callback, stop_event, name, runsOn, melody, durations):
    alarm_on = False
    queue_to_use = should_turn_on_db if name == "DB" else should_turn_on_bb
    print(f"Starting {name} loop")
    
    while not stop_event.is_set():
        if not queue_to_use.empty():
            alarm_on = queue_to_use.get()
            if alarm_on:
                db.turn_on()
            else:
                db.turn_off()
            callback(alarm_on, name, False, runsOn)
        
        if name == "BB" and not input_queue.empty():
            wake_up = input_queue.get()
            if wake_up:
                db.play(melody, durations)
            else:
                db.interrupt.put(True)
                db.turn_off()
            callback(wake_up, name, False, runsOn)
        
        if alarm_on:
            time.sleep(10)
            db.turn_off()
            callback(False, name, False, runsOn)
            alarm_on = False
        else:
            time.sleep(delay)

    db.turn_off()
    callback(False, name, True, runsOn)
    GPIO.cleanup()