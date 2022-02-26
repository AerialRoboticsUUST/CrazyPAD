# -*- coding: utf-8 -*-
#
# Based on bitcraze example project:
# https://github.com/bitcraze/crazyflie-lib-python/blob/master/examples/step-by-step/sbs_motion_commander.py

import logging
import time

import csv
from tkinter import Variable

import matplotlib.pyplot as plt

import cflib.crtp
from cflib.crazyflie import Crazyflie
from cflib.crazyflie.syncCrazyflie import SyncCrazyflie
from cflib.crazyflie.log import LogConfig
from cflib.positioning.position_hl_commander import PositionHlCommander
from cflib.utils import uri_helper

# URI to the Crazyflie to connect to
uri = uri_helper.uri_from_env(default='radio://0/80/2M/E7E7E7E7E7')

logging.basicConfig(level=logging.ERROR)

csvfile=open('position.csv', 'w')
csvfile1=open('stabilizer.csv', 'w')
csvfile2=open('motor.csv', 'w')
csvfile3=open('acc.csv', 'w')
csvfile4=open('range.csv', 'w')
csvfile5=open('target.csv', 'w')

def pos():
    fieldnames = ['timestamp', 'stateEstimate.x', 'stateEstimate.y', 'stateEstimate.z']
    position_writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    position_writer.writeheader()

    def log_pos_callback(timestamp, data, logconf):
        data['timestamp']=timestamp
        print(data)
        position_writer.writerow(data)


    logconf = LogConfig(name='Position', period_in_ms=100)
    logconf.add_variable('stateEstimate.x', 'float')
    logconf.add_variable('stateEstimate.y', 'float')
    logconf.add_variable('stateEstimate.z', 'float')
    scf.cf.log.add_config(logconf)
    logconf.data_received_cb.add_callback(log_pos_callback)
    logconf.start()

def stab():
    fieldnames = ['timestamp', 'stabilizer.roll', 'stabilizer.pitch', 'stabilizer.yaw']
    stabilizer_writer = csv.DictWriter(csvfile1, fieldnames=fieldnames)
    stabilizer_writer.writeheader()

    def log_stab_callback(timestamp, data, logconf):
        data['timestamp']=timestamp
        print(data)
        stabilizer_writer.writerow(data)

    lg_stab = LogConfig(name='Stabilizer', period_in_ms=100)
    lg_stab.add_variable('stabilizer.roll', 'float')
    lg_stab.add_variable('stabilizer.pitch', 'float')
    lg_stab.add_variable('stabilizer.yaw', 'float')
    scf.cf.log.add_config(lg_stab)
    lg_stab.data_received_cb.add_callback(log_stab_callback)
    lg_stab.start()

def mot():
    fieldnames = ['timestamp', 'motor.m1', 'motor.m2', 'motor.m3', 'motor.m4']
    motor_writer = csv.DictWriter(csvfile2, fieldnames=fieldnames)
    motor_writer.writeheader()

    def log_motor_callback(timestamp, data, logconf):
        data['timestamp']=timestamp
        print(data)
        motor_writer.writerow(data)

    lg_motor = LogConfig(name='motor', period_in_ms=100)
    lg_motor.add_variable('motor.m1', 'uint32_t')
    lg_motor.add_variable('motor.m2', 'uint32_t')
    lg_motor.add_variable('motor.m3', 'uint32_t')
    lg_motor.add_variable('motor.m4', 'uint32_t')
    scf.cf.log.add_config(lg_motor)
    lg_motor.data_received_cb.add_callback(log_motor_callback)
    lg_motor.start()

def acc():
    fieldnames = ['timestamp', 'acc.x', 'acc.y', 'acc.z']
    acc_writer = csv.DictWriter(csvfile3, fieldnames=fieldnames)
    acc_writer.writeheader()

    def log_acc_callback(timestamp, data, logconf):
        data['timestamp']=timestamp
        print(data)
        acc_writer.writerow(data)

    lg_acc = LogConfig(name='acc', period_in_ms=100)
    lg_acc.add_variable('acc.x', 'float')
    lg_acc.add_variable('acc.y', 'float')
    lg_acc.add_variable('acc.z', 'float')
    scf.cf.log.add_config(lg_acc)
    lg_acc.data_received_cb.add_callback(log_acc_callback)
    lg_acc.start()

def range():
    fieldnames = ['timestamp', 'range.zrange',]
    range_writer = csv.DictWriter(csvfile4, fieldnames=fieldnames)
    range_writer.writeheader()

    def log_range_callback(timestamp, data, logconf):
        data['timestamp']=timestamp
        print(data)
        range_writer.writerow(data)

    lg_range = LogConfig(name='range', period_in_ms=100)
    lg_range.add_variable('range.zrange', 'float')
    scf.cf.log.add_config(lg_range)
    lg_range.data_received_cb.add_callback(log_range_callback)
    lg_range.start()   

def target():
    fieldnames = ['timestamp', 'ctrltarget.ax', 'ctrltarget.ay', 'ctrltarget.az', 'ctrltarget.vx', 'ctrltarget.vy', 'ctrltarget.vz']
    target_writer = csv.DictWriter(csvfile5, fieldnames=fieldnames)
    target_writer.writeheader()

    def log_target_callback(timestamp, data, logconf):
        data['timestamp']=timestamp
        print(data)
        target_writer.writerow(data)

    lg_target = LogConfig(name='target', period_in_ms=100)
    lg_target.add_variable('ctrltarget.ax', 'float')
    lg_target.add_variable('ctrltarget.ay', 'float')
    lg_target.add_variable('ctrltarget.az', 'float')
    lg_target.add_variable('ctrltarget.vx', 'float')
    lg_target.add_variable('ctrltarget.vy', 'float')
    lg_target.add_variable('ctrltarget.vz', 'float')
    scf.cf.log.add_config(lg_target)
    lg_target.data_received_cb.add_callback(log_target_callback)
    lg_target.start()

if __name__ == '__main__':
    cflib.crtp.init_drivers()

    cf = Crazyflie(rw_cache='./cache')
    
    with SyncCrazyflie(uri, cf=cf) as scf:
        
        pos()
        stab()
        mot()
        acc()
        range()
        target()

        with PositionHlCommander(scf, default_height=0.5, controller=PositionHlCommander.CONTROLLER_PID) as pc:
            pc.go_to( x=0.0, y=0.0, velocity=0.3)
            pc.go_to( x=1.5, y=0.0, velocity=0.3)
            pc.land()
            time.sleep(5)
            pc.take_off( height=0.5, velocity=0.3)
            pc.go_to( x=0.0, y=0.0, velocity=0.3)
            pc.land()

    csvfile.close()
    csvfile1.close()
    csvfile2.close()
    csvfile3.close()
    csvfile4.close()
    csvfile5.close()