# -*- coding: utf-8 -*-
#
# Based on bitcraze example project:
# https://github.com/bitcraze/crazyflie-lib-python/blob/master/examples/step-by-step/sbs_motion_commander.py

import logging
import sys
import time

import csv

from threading import Event

import cflib.crtp
from cflib.crazyflie import Crazyflie
from cflib.crazyflie.syncCrazyflie import SyncCrazyflie
from cflib.positioning.motion_commander import MotionCommander
from cflib.utils import uri_helper
from cflib.utils.multiranger import Multiranger
from cflib.crazyflie.log import LogConfig

URI = uri_helper.uri_from_env(default='radio://0/80/2M/E7E7E7E7E7')

csvfile=open('motion_o.csv', 'w')
fieldnames = ['timestamp', 'stateEstimate.x', 'stateEstimate.y', 'stateEstimate.z']
motion_writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

motion_writer.writeheader()

csvfile1=open('motor_o.csv', 'w')
fieldnames = ['timestamp', 'motor.m1', 'motor.m2', 'motor.m3', 'motor.m4']
motor_writer = csv.DictWriter(csvfile1, fieldnames=fieldnames)

motor_writer.writeheader()


def log_stab_callback(timestamp, data, logconf):
    print('[%d][%s]: %s' % (timestamp, logconf.name, data))

def log_pos_callback(timestamp, data, logconf):
    data['timestamp']=timestamp
    print(data)
    position_writer.writerow(data)

def log_motor_callback(timestamp, data, logconf):
    data['timestamp']=timestamp
    motor_writer.writerow(data)
    print(data)
    
DEFAULT_HEIGHT = 0.2

deck_attached_event = Event()
logging.basicConfig(level=logging.ERROR)    
       
def is_close(range):
    MIN_DISTANCE = 0.3  # m

    if range is None:
        return False
    else:
        return range < MIN_DISTANCE
        
def move_linear_simple(scf):
    with MotionCommander(scf, default_height=DEFAULT_HEIGHT) as mc:
        with Multiranger(scf) as multiranger:
            time.sleep(2)
            mc.forward(0.05, velocity=0.3)
            keep_flying = True
            
            a=1
            while (a<30) and keep_flying:
                mc.forward(0.05, velocity=0.3)
                # time.sleep(1)                   
                if is_close(multiranger.front):
                   mc.move_distance(-0.05, 0.0, 0.0) 
                   time.sleep(1)
                   print ( 'Obstacle placed close to the splitting point' )
                   
                   if is_close(multiranger.left):                   
                      MIN_DISTANCE = 0.5
                      
                      if range is None:
                          return False
                      else:
                          mc.turn_right(angle_degrees=90)
                          mc.forward(0.05, velocity=0.3)
                          print ('turn right')
                if is_close(multiranger.front):
                   mc.move_distance(-0.05, 0.0, 0.0)
                   time.sleep(1)                 
                   if is_close(multiranger.right):                   
                      MIN_DISTANCE = 0.5
                      
                      if range is None:                 
                          return False 
                      else:
                          mc.turn_left(angle_degrees=90)    
                          mc.forward(0.05, velocity=0.3)
                          print ('turn left')     
                                                      
                if is_close(multiranger.back):
                   mc.move_distance(0.05, 0.0, 0.0)
                   keep_flying = True
                   print ('front')
                if is_close(multiranger.left):
                   mc.move_distance(0.0, -0.05, 0.0)
                   mc.forward(0.05, velocity=0.3)
                   print ('right')
                if is_close(multiranger.right):
                   mc.move_distance(0.0, 0.05, 0.0)
                   mc.forward(0.05, velocity=0.3)
                   print ('left')
                
            while keep_flying:
                VELOCITY = 0.5
                velocity_x = 0.1
            a=a+1
  

def take_off_simple(scf):
    ...
    
def log_pos_callback(timestamp, data, logconf):
    print(data)
    global position_estimate
    position_estimate[0] = data['stateEstimate.x']
    position_estimate[1] = data['stateEstimate.y']


def param_deck_flow(name, value_str):
    value = int(value_str)
    print(value)
    global is_deck_attached
    if value:
        is_deck_attached = True
        print('Deck is attached!')
    else:
        is_deck_attached = False
        print('Deck is NOT attached!')
        
if __name__ == '__main__':
    cflib.crtp.init_drivers()
    
    cf = Crazyflie(rw_cache='./cache')
    
    with SyncCrazyflie(uri, cf=cf) as scf:
        logconf = LogConfig(name='Position', period_in_ms=100)
        logconf.add_variable('stateEstimate.x', 'float')
        logconf.add_variable('stateEstimate.y', 'float')
        logconf.add_variable('stateEstimate.z', 'float')
        scf.cf.log.add_config(logconf)
        logconf.data_received_cb.add_callback(log_pos_callback)
        logconf.start()

        lg_stab = LogConfig(name='Stabilizer', period_in_ms=100)
        lg_stab.add_variable('stabilizer.roll', 'float')
        lg_stab.add_variable('stabilizer.pitch', 'float')
        lg_stab.add_variable('stabilizer.yaw', 'float')
        scf.cf.log.add_config(lg_stab)
        lg_stab.data_received_cb.add_callback(log_stab_callback)
        lg_stab.start()

        lg_motor = LogConfig(name='motor', period_in_ms=100)
        lg_motor.add_variable('motor.m1', 'uint32_t')
        lg_motor.add_variable('motor.m2', 'uint32_t')
        lg_motor.add_variable('motor.m3', 'uint32_t')
        lg_motor.add_variable('motor.m4', 'uint32_t')
        scf.cf.log.add_config(lg_motor)
        lg_motor.data_received_cb.add_callback(log_motor_callback)
        lg_motor.start()
        

        take_off_simple(scf)
        move_linear_simple(scf)
        logconf.stop()
        with Multiranger(scf) as multiranger:
                keep_flying = True
       

        move_linear_simple(scf)
        csvfile.close()
        csvfile1.close()
