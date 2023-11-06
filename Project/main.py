from components.buzzer.buzzer import Buzzer
from components.dht.dht import DHT
from components.door_light.dioda import Dioda
from components.door_membrane_switch.membrane_switch import MembraneSwitch
from components.door_sensor.door_sensor import MotionSensor
from components.door_ultrasonic_sensor.ultrasonic_sensor import UltrasonicSensor
from project_settings.settings import load_settings


def run_door_light(settings):
    door_light_settings = settings['DL']
    door_light = Dioda(door_light_settings['pin'], door_light_settings['simulated'])
    door_light.run([])


def run_door_motion(settings):
    motion_sensor_settings = settings['DS1']
    motion_sensor = MotionSensor(motion_sensor_settings['pin'], motion_sensor_settings['simulated'])
    motion_sensor.run([])


def run_buzzer(settings):
    buzzer_settings = settings['DS1']
    door_buzzer = Buzzer(buzzer_settings['pin'], buzzer_settings['simulated'])
    door_buzzer.run([])


def run_uds(settings):
    uds_settings = settings['DUS1']
    uds = UltrasonicSensor(uds_settings['trigger_pin'], uds_settings['echo_pin'], uds_settings['simulated'])
    uds.run([])


def run_membrane_switch(settings):
    dms_settings = settings['DMS']
    uds = MembraneSwitch(dms_settings['pin'], dms_settings['simulated'])
    uds.run([])


def run_dht(settings):
    dht_settings = settings['RDHT1']
    dht = DHT(dht_settings['pin'], dht_settings['simulated'])
    dht.run([])


def menu_print():
    print("Door light  --> 1")
    print("Door motion --> 2")
    print("Buzzer      --> 3")
    print("UDS         --> 4")
    print("MembraneSW  --> 5")
    print("DHT         --> 6")
    print("izlazak     --> x")


def menu():
    settings = load_settings()
    while True:
        menu_print()
        choice = input("Unesite izbor: ")

        if choice.strip().lower() == "1":
            run_door_light(settings)
        elif choice.strip().lower() == "2":
            run_door_motion(settings)
        elif choice.strip().lower() == "3":
            run_buzzer(settings)
        elif choice.strip().lower() == "4":
            run_uds(settings)
        elif choice.strip().lower() == "5":
            run_membrane_switch(settings)
        elif choice.strip().lower() == "6":
            run_dht(settings)
        else:
            break


if __name__ == '__main__':

    menu()
