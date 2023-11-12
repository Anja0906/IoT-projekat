import threading
import time

from sensors.s_simulators.dht import run_dht_simulator


def dht_callback(humidity, temperature, code):
    t = time.localtime()
    print("=" * 20)
    print(f"Timestamp: {time.strftime('%H:%M:%S', t)}")
    print(f"Code: {code}")
    print(f"Humidity: {humidity}%")
    print(f"Temperature: {temperature}°C\n")


def run_dht(settings, threads, stop_event, code):
    if settings['simulated']:
        print("Starting " + code + " simulator")
        dht_thread = threading.Thread(target=run_dht_simulator, args=(5, dht_callback, stop_event, code))
        dht_thread.start()
        threads.append(dht_thread)
        print(code + " simulator started\n")
    else:
        from sensors.s_components.dht import run_dht_loop, DHT
        print("Starting " + code + " loop")
        dht = DHT(settings['pin'])
        dht_thread = threading.Thread(target=run_dht_loop, args=(dht, 5, dht_callback, stop_event, code))
        dht_thread.start()
        threads.append(dht_thread)
        print(code + " loop started")
