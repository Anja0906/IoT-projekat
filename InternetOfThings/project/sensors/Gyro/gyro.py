#!/usr/bin/env python3
import MPU6050 
import time
import os
import json


accel = [0]*3               
gyro = [0]*3                


def run_gyro_loop(mpu, delay, callback, stop_event, publish_event, settings):
    mpu.dmp_initialize()
    while True:
        accel = mpu.get_acceleration()     
        gyro = mpu.get_rotation()          
        accel = [a/16384.0 for a in accel]
        gyro = [g/131.0 for g in gyro]
        callback(accel, gyro, publish_event, settings)
        os.system('clear')
        if stop_event.is_set():
            break
        time.sleep(delay)


