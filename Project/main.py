# from components.buzzer.buzzer import Buzzer
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


# def run_buzzer(settings):
#     buzzer_settings = settings['DS1']
#     door_buzzer = Buzzer(buzzer_settings['pin'], buzzer_settings['simulated'])
#     door_buzzer.run([])


def run_uds(settings):
    uds_settings = settings['DUS1']
    uds = UltrasonicSensor(uds_settings['trigger_pin'], uds_settings['echo_pin'], uds_settings['simulated'])
    uds.run([])


def run_membrane_switch(settings):
    dms_settings = settings['DMS']
    uds = MembraneSwitch(dms_settings['pin'], dms_settings['simulated'])
    uds.run([])


def run_dht(settings):
    dht_settings = settings['DHT']
    dht = DHT(dht_settings['pin'], dht_settings['simulated'])
    dht.run([])


if __name__ == '__main__':
    settings = load_settings()
    # run_door_light(settings)
    # run_door_motion(settings)
    # run_buzzer(settings)
    # run_uds(settings)
    #run_membrane_switch(settings)
    #run_dht(settings)
