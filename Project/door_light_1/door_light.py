from simulation.dioda_simulation import generate_values
from project_settings.settings import load_settings
import threading
import time



def run_dht(settings, threads):
        if settings['simulated']:
            print("Starting dioda sumilator")
            dioda_thread = threading.Thread(target = generate_values(), args=())
            dioda_thread.start()
            threads.append(dioda_thread)
            print("Dioda sumilator started")
        else:
            from sensor.dioda import Dioda, run_dioda_loop
            print("Starting dht1 loop")
            dioda = Dioda(settings['pin'])
            dioda_thread = threading.Thread(target=dioda.run_dioda_loop(), args=())
            dioda_thread.start()
            threads.append(dioda_thread)
            print("Dioda loop started")

settings = load_settings()
print(settings['simulated'])
run_dht(settings,[])