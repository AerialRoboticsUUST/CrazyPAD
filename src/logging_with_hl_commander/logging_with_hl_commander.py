# -*- coding: utf-8 -*-
#
# Based on bitcraze example project:
# https://github.com/bitcraze/crazyflie-lib-python/blob/master/examples/step-by-step/sbs_motion_commander.py

from fileinput import filename
import logging
import time

import csv

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

# Log variables
class LogVaraible():
    def __init__(self, name, type):
        self.name = name
        self.type = type

# File logger
class FileLogger(object):
    def __init__(self, logConf, fileName, logVariables):
        self._logConf = logConf

        fieldnames = ['timestamp']
        for logVar in logVariables:
            self._logConf.add_variable(logVar.name, logVar.type)
            fieldnames.append(logVar.Name)

        
        self._csvfile = open(fileName, 'w')
        self._data_writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        self._data_writer.writeheader()

        def log_callback(timestamp, data):
            data['timestamp']=timestamp
            self._data_writer.writerow(data)
            print(data)
            
        self._logConf.data_received_cb.add_callback(log_callback)

    def start(self, crazyflie):
        crazyflie.log.add_config(self._logConf)
        self._logConf.start()

    def stop(self):
        self._logConf.stop()
        self._csvfile.close()    

def init_loggers():
    loggers = []

    logconf = LogConfig(name='Position', period_in_ms=100)
    logvars = [
        LogVaraible('stateEstimate.x', 'float'),
        LogVaraible('stateEstimate.x', 'float'),
        LogVaraible('stateEstimate.x', 'float'),
    ]
    loggers.append(FileLogger(logconf, 'position.csv', logvars))

    logconf = LogConfig(name='Stabilizer', period_in_ms=100)
    logvars = [
        LogVaraible('stabilizer.roll', 'float'),
        LogVaraible('stabilizer.pitch', 'float'),
        LogVaraible('stabilizer.yaw', 'float'),
    ]
    loggers.append(FileLogger(logconf, 'stabilizer.csv', logvars))

    logconf = LogConfig(name='Motor', period_in_ms=100)
    logvars = [
        LogVaraible('motor.m1', 'uint32_t'),
        LogVaraible('motor.m2', 'uint32_t'),
        LogVaraible('motor.m3', 'uint32_t'),
        LogVaraible('motor.m4', 'uint32_t'),
    ]
    loggers.append(FileLogger(logconf, 'motor.csv', logvars))

    return loggers

def start_logging(cf, loggers):
    for logger in loggers:
        logger.start(cf)    

def stop_logging(loggers):
    for logger in loggers:
        logger.stop() 

if __name__ == '__main__'
    cflib.crtp.init_drivers()

    cf = Crazyflie(rw_cache='./cache')
    
    with SyncCrazyflie(uri, cf=cf) as scf:
        loggers = init_loggers()
        start_logging(cf, loggers)

        with PositionHlCommander(scf, default_height=0.5, controller=PositionHlCommander.CONTROLLER_PID) as pc:
            pc.go_to( x=0.0, y=0.0, velocity=0.3)
            pc.go_to( x=1.5, y=0.0, velocity=0.3)
            pc.land()
            time.sleep(5)
            pc.take_off( height=0.5, velocity=0.3)
            pc.go_to( x=0.0, y=0.0, velocity=0.3)
            pc.land()

        stop_logging(loggers)
    