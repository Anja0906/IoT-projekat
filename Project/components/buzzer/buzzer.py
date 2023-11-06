# import time
# import threading
# import winsound
#
#
# class Buzzer(object):
#     def __init__(self, pin, simulated):
#         self.pin = pin
#         self.simulated = simulated
#         self.sample_rate = 44100
#
#     def buzz(self, pitch, duration):
#         period = 1.0 / pitch
#         delay = period / 2
#         cycles = int(duration * pitch)
#         for i in range(cycles):
#             GPIO.output(self.pin, True)
#             time.sleep(delay)
#             GPIO.output(self.pin, False)
#             time.sleep(delay)
#
#     def run_buzzer_loop(self):
#         from RPi.GPIO import GPIO
#         GPIO.setmode(GPIO.BCM)
#         GPIO.setup(self.pin, GPIO.OUT)
#         try:
#             while True:
#                 pitch = 440
#                 duration = 0.1
#                 self.buzz(pitch, duration)
#                 time.sleep(1)
#         except KeyboardInterrupt:
#             GPIO.cleanup()
#
#     def buzz_simulation(self, pitch, duration):
#         winsound.Beep(int(pitch), int(duration * 1000))
#
#     def generate_values(self):
#         try:
#             while True:
#                 pitch = 440
#                 duration = 100
#                 self.buzz_simulation(pitch, duration)
#                 time.sleep(1)
#         except KeyboardInterrupt:
#             pass
#
#     def run(self, threads):
#         stop_event = threading.Event()
#         try:
#             if self.simulated:
#                 print("Starting buzzer simulator")
#                 buzzer_thread = threading.Thread(target=self.generate_values)
#                 buzzer_thread.start()
#                 threads.append(buzzer_thread)
#             elif not self.simulated:
#                 print("Starting buzzer loop")
#                 buzzer_thread = threading.Thread(target=self.run_buzzer_loop)
#                 buzzer_thread.start()
#                 threads.append(buzzer_thread)
#             else:
#                 print("Self.simulated is none")
#         except KeyboardInterrupt:
#             for t in threads:
#                 stop_event.set()
#
