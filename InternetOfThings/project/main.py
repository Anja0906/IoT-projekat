import json
import multiprocessing
import threading
import paho.mqtt.client as mqtt
from datetime import datetime, timedelta
from time import sleep

from components.button import run_button
from components.ms import run_ms
from components.dioda import run_dioda
from components.uds import run_uds
from components.dht import run_dht
from components.pir import run_pir
from components.buzzer import run_buzzer
from components.gyro import run_gyro
from components.lcd import run_lcd
from components.b4sd import run_b4sd
from components.IR import run_infrared
from components.rgb import run_rgb
from settings.settings import load_settings,HOSTNAME,PORT

try:
    import RPi.GPIO as GPIO
    GPIO.setmode(GPIO.BCM)
except ImportError:
    pass

pi_light_pipe, light_pipe = multiprocessing.Pipe()
buzzer_stop_event = threading.Event()
stop_event = threading.Event()
mqtt_client = mqtt.Client()
buzzer_active = False
bb_alarm_time = "21:39"

def on_connect(client, userdata, flags, rc):
    client.subscribe("pi1")
    client.subscribe("front-bb-on")
    client.subscribe("front-bb-off")
    client.subscribe("pi3")

mqtt_client.on_connect = on_connect
mqtt_client.on_message = lambda client, userdata, msg: update_data(msg.topic, json.loads(msg.payload.decode('utf-8')))

def connect_mqtt():
    mqtt_client.connect(HOSTNAME, PORT, 60)
    mqtt_client.loop_start()

def menu():
    print("=" * 10 + "  MENU  " + "=" * 10)
    print("-- Enter B to activate buzzer --")
    print("-- Enter D to deactivate buzzer --")
    print("-- Enter L to change light state --")
    print("-- Enter X to stop all devices --")
    print("=" * 30)

def user_inputs(data):
    global buzzer_active, db_settings
    if data["trigger"] == "B" and not buzzer_active:
        print("BUZZER RADI")
        buzzer_stop_event.clear()
        run_buzzer(db_settings, threads, buzzer_stop_event)
        buzzer_active = True
    elif data["trigger"] == "D":
        buzzer_stop_event.set()
        buzzer_active = False
    elif data["trigger"] == "X":
        stop_event.set()
        buzzer_stop_event.set()
    elif data["trigger"] == "L":
        pi_light_pipe.send("l")


def update_data(topic, data):
    print("bb data: ", data, "received from topic " + topic)
    if topic == "front-bb-on":
        global bb_alarm_time
        bb_alarm_time = data["time"]
    elif topic == "front-bb-off":
        buzzer_stop_event.set()
    elif topic == "pi3":
        user_inputs(data)

def run_alarm_clock(bb_settings, threads, buzzer_stop_event):
    global mqtt_client
    is_active = False
    time_difference = timedelta(seconds=7)
    while True:
        target_time = datetime.strptime(bb_alarm_time, "%H:%M").time()
        current_time = datetime.now().time()

        delta_target_time = datetime.combine(datetime.today(), target_time) + time_difference
        max_target_time = delta_target_time.time()

        if target_time <= current_time <= max_target_time and not is_active:
            print("IDE ALARM NA MAKS")
            buzzer_stop_event.clear()
            run_buzzer(bb_settings, threads, buzzer_stop_event)
            is_active = True
            mqtt_client.publish("front-bb-on", json.dumps({"time": ""}))
        if buzzer_stop_event.is_set():
            is_active = False
        sleep(5)

def run_pi1(settings, threads, stop_event, pi_light_pipe):
    dht1_settings = settings.get('DHT1')
    dht2_settings = settings.get('DHT2')
    uds1_settings = settings.get('DUS1')
    rpir1_settings = settings.get('RPIR1')
    rpir2_settings = settings.get('RPIR2')
    dpir1_settings = settings.get('DPIR1')
    ds1_settings = settings.get('DS1')
    ms_settings = settings.get('DMS')
    db_settings = settings.get('DB')
    dl_settings = settings.get('DL')

    if dht1_settings:
        run_dht(dht1_settings, threads, stop_event)
    if dht2_settings:
        run_dht(dht2_settings, threads, stop_event)
    if uds1_settings:
        run_uds(uds1_settings, threads, stop_event)
    if rpir1_settings:
        run_pir(rpir1_settings, threads, stop_event)
    if rpir2_settings:
        run_pir(rpir2_settings, threads, stop_event)
    if dpir1_settings:
        run_pir(dpir1_settings, threads, stop_event)
    if ds1_settings:
        run_button(ds1_settings, threads, stop_event)
    if ms_settings:
        run_ms(ms_settings, threads, stop_event)
    if pi_light_pipe and dl_settings:
        run_dioda(pi_light_pipe, dl_settings, threads, stop_event)

def run_pi2(settings, threads, stop_event):
    gdht_settings = settings.get('GDHT')
    rdht3_settings = settings.get('RDHT3')
    uds2_settings = settings.get('DUS2')
    rpir3_settings = settings.get('RPIR3')
    dpir2_settings = settings.get('DPIR2')
    glcd_settings = settings.get('GLCD')
    gsg_settings = settings.get('GSG')
    ds2_settings = settings.get('DS2')

    if gdht_settings:
        run_dht(gdht_settings, threads, stop_event)
    if rdht3_settings:
        run_dht(rdht3_settings, threads, stop_event)
    if uds2_settings:
        run_uds(uds2_settings, threads, stop_event)
    if rpir3_settings:
        run_pir(rpir3_settings, threads, stop_event)
    if dpir2_settings:
        run_pir(dpir2_settings, threads, stop_event)
    if glcd_settings:
        run_lcd(glcd_settings, threads, stop_event)
    if gsg_settings:
        run_gyro(gsg_settings, threads, stop_event)
    if ds2_settings:
        run_button(ds2_settings, threads, stop_event)

def run_pi3(settings, threads, stop_event, buzzer_stop_event):
    rdht4_settings = settings.get('RDHT4')
    rpir4_settings = settings.get('RPIR4')
    bb_settings = settings.get('BB')
    bir_settings = settings.get('BIR')
    brgb_settings = settings.get('BRGB')
    b4sd_settings = settings.get('B4SD')

    if rdht4_settings:
        run_dht(rdht4_settings, threads, stop_event)
    if rpir4_settings:
        run_pir(rpir4_settings, threads, stop_event)
    if bir_settings:
        run_infrared(bir_settings, threads, stop_event)
    if brgb_settings:
        run_rgb(brgb_settings, threads, stop_event,HOSTNAME,PORT)
    if b4sd_settings:
        run_b4sd(b4sd_settings, threads, stop_event,HOSTNAME,PORT)

    alarm_clock_thread = threading.Thread(target=run_alarm_clock, args=(bb_settings, threads, buzzer_stop_event))
    alarm_clock_thread.start()
    threads.append(alarm_clock_thread)

if __name__ == "__main__":
    print('Starting PI')
    connect_mqtt()
    menu()
    settings = load_settings()
    threads = []
    db_settings = settings.get('DB')

    try:
        run_pi1(settings, threads, stop_event, pi_light_pipe)
        run_pi2(settings, threads, stop_event)
        run_pi3(settings, threads, stop_event, buzzer_stop_event)

        while True:
            user_input = input().strip().upper()
            if user_input == "X":
                stop_event.set()

    except KeyboardInterrupt:
        print('\nStopping app')
        stop_event.set()
        buzzer_stop_event.set()
        for t in threads:
            t.join()
