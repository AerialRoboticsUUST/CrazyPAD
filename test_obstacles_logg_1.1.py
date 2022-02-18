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
from cflib.crazyflie.syncLogger import SyncLogger

URI = uri_helper.uri_from_env(default='radio://0/80/2M/E7E7E7E7E7')

def simple_log(scf, logconf):
    with SyncLogger(scf, lg_stab) as logger:

        for log_entry in logger:

            timestamp = log_entry[0]
            data = log_entry[1]
            logconf_name = log_entry[2]

            print('[%d][%s]: %s' % (timestamp, logconf_name, data))

            break

DEFAULT_HEIGHT = 0.2

deck_attached_event = Event()
logging.basicConfig(level=logging.ERROR)

position_estimate = [0, 0]

def log_stab_callback(timestamp, data, logconf):
    print(data)
    global position_estimate
    position_estimate[0] = data['stateEstimate.x']
    position_estimate[1] = data['stateEstimate.y']

def simple_log_async(scf, logconf):
    cf = scf.cf
    cf.log.add_config(logconf)
    logconf.data_received_cb.add_callback(log_stab_callback)
    logconf.start()
    time.sleep(5)
    logconf.stop()
    
     # Callback called when the connection is established to the Crazyflie
def connected(link_uri):
    crazyflie.log.add_config(logconf)

    if logconf.valid:
       logconf.data_received_cb.add_callback(data_received_callback)
       logconf.error_cb.add_callback(logging_error)
       logconf.start()
    else:
       print ("One or more of the variables in the configuration was not found in log TOC. No logging will be possible.")

def data_received_callback(timestamp, data, logconf):
       print ('[%d][%s]: %s' % (timestamp, logconf.name, data))

def logging_error(logconf, msg):
       print ('Error when logging %s' % logconf.name)
       
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
            #while keep_flying:
                # VELOCITY = 0.3
                # velocity_x = 0.1
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
  

def move_box_limit(scf):
    with MotionCommander(scf, default_height=DEFAULT_HEIGHT) as mc:
        body_x_cmd = 0.2
        body_y_cmd = 0.1
        max_vel = 0.2

        while (1):
            '''if position_estimate[0] > BOX_LIMIT:
                mc.start_back()
            elif position_estimate[0] < -BOX_LIMIT:
                mc.start_forward()
            '''

            if position_estimate[0] > BOX_LIMIT:
                body_x_cmd = -max_vel
            elif position_estimate[0] < -BOX_LIMIT:
                body_x_cmd = max_vel
            if position_estimate[1] > BOX_LIMIT:
                body_y_cmd = -max_vel
            elif position_estimate[1] < -BOX_LIMIT:
                body_y_cmd = max_vel

            mc.start_linear_motion(body_x_cmd, body_y_cmd, 0)

            time.sleep(0.1)
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
    
    with SyncCrazyflie(URI, cf=Crazyflie(rw_cache='./cache')) as scf:      
        scf.cf.param.add_update_callback(group='deck', name='bcFlow2',
                                         cb=param_deck_flow)
        time.sleep(1)

        logconf = LogConfig(name='Position', period_in_ms=500)
        logconf.add_variable('stateEstimate.x', 'float')
        logconf.add_variable('stateEstimate.y', 'float')
        logconf.add_variable('stateEstimate.z', 'float')
        logconf.add_variable('stabilizer.roll', 'float')
        logconf.add_variable('stabilizer.pitch', 'float')
        logconf.add_variable('stabilizer.yaw', 'float')
        scf.cf.log.add_config(logconf)
        logconf.data_received_cb.add_callback(log_pos_callback)
        logconf.start()
        
        with open('names1.csv', 'w') as csvfile:
            fieldnames = ['x', 'y', 'z']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            writer.writerow({'x': 'stateEstimate.x', 'y': 'stateEstimate.y', 'z': 'stateEstimate.z'})
            print("Writing complete")    
        
        take_off_simple(scf)
        move_linear_simple(scf)
        logconf.stop()
        with Multiranger(scf) as multiranger:
                keep_flying = True
       

        move_linear_simple(scf)
