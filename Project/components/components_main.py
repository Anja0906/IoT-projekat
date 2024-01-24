import sys
import threading
from components.actuators.Dioda.dioda_component import run_dl
from components.sensors.Button.button_component import run_ds
from components.sensors.Clock.clock_component import run_clock
from components.sensors.DHT.dht_component import run_dht
from components.sensors.DUS.dus_component import run_dus
from components.sensors.Gyro.gyro_component import run_gyro
from components.sensors.IR.ir_component import run_ir_receiver
from components.sensors.LCD.lcd_component import run_lcd
from components.sensors.MembraneSwitch.membrane_switch_component import run_dms
from components.sensors.PIR.pir_component import run_dpir
from components.sensors.RGB_Dioda.rgb_component import run_rgb_light
from project_settings.settings import load_settings
import paho.mqtt.client as mqtt
#MQTT ------------------------------------------------------------
mqtt_client = mqtt.Client()
mqtt_client.connect("localhost", 1883, 60)
mqtt_client.loop_start()

topics = [
    "Temperature/Sensors",
    "Humidity/Sensors",
    "Motion/Sensors",
    "DoorSensor/Sensors",
    "DoorUltraSonic/Sensors",
    "MembraneSwitch/Sensors",
    "Buzzer/Sensors",
    "DoorLight/Sensors",
    "Gyro/Sensors",
    "LCD/Sensors",
    "Clock/Sensors",
    "RGB/Sensors",
    "BedroomInfrared/Sensors"
]


ds1_pressed_event = threading.Event()
alarm_event = threading.Event()
read_from_db_event_dus1 = threading.Event()
pir1_motion_detected_event = threading.Event()

ds2_pressed_event = threading.Event()
pir2_motion_detected_event = threading.Event()
read_from_db_event_dus2 = threading.Event()

ir_changed_event = threading.Event()
alarm_clock = threading.Event()

def on_message(client, userdata, message):
    if message.topic == "alarm":
        alarm_event.set()
        # alarm_clock.set()
        print(f"Topic: {message.topic}\nPoruka: {message.payload.decode()}")
    if message.topic == "ds1":
        ds1_pressed_event.set()
        print(f"Topic: {message.topic}\nPoruka: {message.payload.decode()}")
    if message.topic == "ds2":
        ds2_pressed_event.set()
        print(f"Topic: {message.topic}\nPoruka: {message.payload.decode()}")

# Dodavanje callback funkcije za pristigle poruke
mqtt_client.on_message = on_message
mqtt_client.subscribe("alarm")
mqtt_client.subscribe("ds1")
mqtt_client.subscribe("ds2")
def on_connect(client, userdata, flags, rc):
    for topic in topics:
        client.subscribe(topic)

mqtt_client = mqtt.Client()
mqtt_client.connect("localhost", 1883, 60)
mqtt_client.loop_start()
mqtt_client.on_connect = on_connect
#MQTT ------------------------------------------------------------


#PI Functions ---------------------------------------------------------------------------
def run_pi_1(settings, threads, stop_event,mqtt_client):
    run_ds(settings['DS1'], threads, ds1_pressed_event, 'DS1',mqtt_client)
    run_dl(settings["DL"], threads, pir1_motion_detected_event, "DL")
    run_dus(settings['DUS1'], threads, 'DUS1')
    run_dpir(settings['DPIR1'], threads, pir1_motion_detected_event, 'DPIR1')
    run_dms(settings['DMS'], threads, stop_event, 'DMS')
    run_dpir(settings['RPIR1'], threads, stop_event, 'RPIR1')
    run_dpir(settings['RPIR2'], threads, stop_event, 'RPIR2')
    run_dht(settings['RDHT1'], threads, 'RDHT1')
    run_dht(settings['RDHT2'], threads, 'RDHT2')
    # run db
    while True:
        alarm_event.wait()
        print("\n Oglasio see!!!!!!!!!!!!")
        alarm_event.clear()

#Todo: Napraviti globalnu promenljivu za button_pressed koja simulira stisak dugmeta i setuje ds1_pressed_event
def run_pi_2(settings, threads, stop_event,mqtt_client):
    run_ds(settings['DS2'], threads, ds2_pressed_event, 'DS2',mqtt_client)
    run_dus(settings['DUS2'], threads, 'DUS2')
    run_dpir(settings['DPIR2'], threads, pir1_motion_detected_event, 'DPIR2')
    run_dht(settings['GDHT'], threads, 'GDHT')
    run_lcd(settings['GLCD'], threads, 'GLCD')
    run_gyro(settings['GSG'], threads, stop_event, 'GSG')
    run_dpir(settings['RPIR3'], threads, stop_event, 'RPIR3')
    run_dht(settings['RDHT3'], threads, 'RDHT3')


def run_pi_3(settings, threads, stop_event,mqtt_client):
    run_dpir(settings['RPIR4'], threads, stop_event, 'RPIR4')
    run_dht(settings['RDHT4'], threads, 'RDHT4')
    run_clock(settings['B4SD'], threads, alarm_clock, 'B4SD')
    run_ir_receiver(settings['BIR'], threads, ir_changed_event, 'BIR')
    run_rgb_light(settings['BRGB'], threads, ir_changed_event, 'BRGB')
    # run BB


def run_system(settings, threads, stop_event,mqtt_client):
    # run_pi_1(settings, threads, stop_event,mqtt_client)
    # run_pi_2(settings, threads, stop_event,mqtt_client)
    run_pi_3(settings, threads, stop_event,mqtt_client)
    for thread in threads:
        thread.join()
#PI Functions ---------------------------------------------------------------------------


if __name__ == "__main__":

    settings = load_settings()
    threads = []
    stop_event = threading.Event()

    try:
        while True:
            run_system(settings, threads, stop_event,mqtt_client)
            stop_event.clear()
            threads = []

    except KeyboardInterrupt:
        print('Stopping app')
        for t in threads:
            stop_event.set()
        sys.exit(0)
