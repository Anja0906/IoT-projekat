import threading

from sensors.s_simulators.rgb_dioda import run_rgb_dioda_simulation


def run_dus(settings, threads, stop_event, code):
    if settings['simulated']:
        print("Starting " + code + " simulator")
        rgb_thread = threading.Thread(target=run_rgb_dioda_simulation, args=())
        rgb_thread.start()
        threads.append(rgb_thread)
        print(code + " simulator started\n")
    else:
        from sensors.s_components.rgb_dioda import run_rgb_dioda
        print("Starting " + code + " loop")
        rgb_thread = threading.Thread(target=run_rgb_dioda, args=())
        rgb_thread.start()
        threads.append(rgb_thread)
        print(code + " loop started")