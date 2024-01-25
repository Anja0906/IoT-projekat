import sys
import threading

from components.actuators.Buzzer.buzzer_component import run_db
from components.actuators.Dioda.dioda_component import run_dl
from components.broker_settings import HOSTNAME, PORT
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

# MQTT ------------------------------------------------------------
mqtt_client = mqtt.Client()
mqtt_client.connect(HOSTNAME, PORT, 60)
mqtt_client.loop_start()

mqtt_client.subscribe("alarm")
mqtt_client.subscribe("ds1")
mqtt_client.subscribe("ds2")
mqtt_client.subscribe("CodeChanged")
mqtt_client.subscribe("budilnik/on")
mqtt_client.subscribe("budilnik/off")

budilnik_event = threading.Event()
ds1_pressed_event = threading.Event()
alarm_event = threading.Event()
read_from_db_event_dus1 = threading.Event()
pir1_motion_detected_event = threading.Event()
dms_set_event = threading.Event()

ds2_pressed_event = threading.Event()
pir2_motion_detected_event = threading.Event()
read_from_db_event_dus2 = threading.Event()

ir_changed_event = threading.Event()
alarm_clock = threading.Event()
changed_code = threading.Event()
code = ""


def on_message(client, userdata, message):
    global code
    # if message.topic == "alarm":
    #     alarm_event.set()
    #     print(f"Topic: {message.topic}\nPoruka: {message.payload.decode()}")
    if message.topic == "ds1":
        ds1_pressed_event.set()
        if changed_code.is_set():
            alarm_event.set()
        print(f"Topic: {message.topic}\nPoruka: {message.payload.decode()}")
    if message.topic == "ds2":
        ds2_pressed_event.set()
        if changed_code.is_set():
            alarm_event.set()
        print(f"Topic: {message.topic}\nPoruka: {message.payload.decode()}")
    if message.topic == "budilnik/on":
        budilnik_event.set()
    if message.topic == "budilnik/off":
        budilnik_event.clear()
    if message.topic == "CodeChanged":
        if not changed_code.is_set():
            code = message.payload.decode()
            changed_code.set()
        elif code == message.payload.decode():
            changed_code.clear()
            if alarm_event.is_set(): alarm_event.clear()
        else:
            print("UPALIO SAM ALARM")
            alarm_event.set()


mqtt_client.on_message = on_message


# PI Functions ---------------------------------------------------------------------------
def run_pi_1(settings, threads, stop_event, mqtt_client):
    run_ds(settings['DS1'], threads, ds1_pressed_event, 'DS1')
    run_dl(settings["DL"], threads, pir1_motion_detected_event, "DL")
    run_dus(settings['DUS1'], threads, 'DUS1')
    run_dpir(settings['DPIR1'], threads, pir1_motion_detected_event, 'DPIR1')
    run_dms(settings['DMS'], threads, changed_code, 'DMS')
    run_dpir(settings['RPIR1'], threads, stop_event, 'RPIR1')
    run_dpir(settings['RPIR2'], threads, stop_event, 'RPIR2')
    run_dht(settings['RDHT1'], threads, 'RDHT1')
    run_dht(settings['RDHT2'], threads, 'RDHT2')
    run_db(settings['DB'], threads, alarm_event, alarm_event, "DB")


# Todo: Napraviti globalnu promenljivu za button_pressed koja simulira stisak dugmeta i setuje ds1_pressed_event
def run_pi_2(settings, threads, stop_event, mqtt_client):
    run_ds(settings['DS2'], threads, ds2_pressed_event, 'DS2')
    run_dus(settings['DUS2'], threads, 'DUS2')
    run_dpir(settings['DPIR2'], threads, pir1_motion_detected_event, 'DPIR2')
    run_dht(settings['GDHT'], threads, 'GDHT')
    run_lcd(settings['GLCD'], threads, 'GLCD')
    run_gyro(settings['GSG'], threads, stop_event, 'GSG')
    run_dpir(settings['RPIR3'], threads, stop_event, 'RPIR3')
    run_dht(settings['RDHT3'], threads, 'RDHT3')


def run_pi_3(settings, threads, stop_event, mqtt_client):
    run_dpir(settings['RPIR4'], threads, stop_event, 'RPIR4')
    run_dht(settings['RDHT4'], threads, 'RDHT4')
    run_clock(settings['B4SD'], threads, alarm_clock, 'B4SD')
    run_ir_receiver(settings['BIR'], threads, ir_changed_event, 'BIR')
    run_rgb_light(settings['BRGB'], threads, ir_changed_event, 'BRGB')
    run_db(settings['BB'], threads, alarm_event, budilnik_event, "BB")


def run_system(settings, threads, stop_event, mqtt_client):
    run_pi_1(settings, threads, stop_event, mqtt_client)
    run_pi_2(settings, threads, stop_event, mqtt_client)
    run_pi_3(settings, threads, stop_event, mqtt_client)
    for thread in threads:
        thread.join()


if __name__ == "__main__":
    settings = load_settings()
    threads = []
    stop_event = threading.Event()
    try:
        while True:
            run_system(settings, threads, stop_event, mqtt_client)
            stop_event.clear()
            threads = []

    except KeyboardInterrupt:
        print('Stopping app')
        for t in threads:
            stop_event.set()
        sys.exit(0)
