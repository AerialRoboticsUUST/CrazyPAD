# -*- coding: utf-8 -*-
#
# Based on bitcraze example project:
# https://github.com/bitcraze/crazyflie-lib-python/blob/master/examples/step-by-step/sbs_motion_commander.py

from fileinput import filename
import logging
import time

import csv

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
            fieldnames.append(logVar.name)

        
        self._csvfile = open(fileName, 'w')
        self._data_writer = csv.DictWriter(self._csvfile, fieldnames=fieldnames)
        self._data_writer.writeheader()
            
        self._logConf.data_received_cb.add_callback(self._log_callback)

    def _log_callback(self, timestamp, data, logconf):
            data['timestamp']=timestamp
            self._data_writer.writerow(data)
            print(data)
    
    def start(self, crazyflie):
        crazyflie.log.add_config(self._logConf)
        self._logConf.start()

    def stop(self):
        self._logConf.stop()
        self._logConf.data_received_cb.remove_callback(self._log_callback)
        self._csvfile.close()    

def init_loggers():
    loggers = []

    logconf = LogConfig(name='Acc', period_in_ms=100)
    logvars = [
        LogVaraible('acc.x', 'float'),
        LogVaraible('acc.y', 'float'),
        LogVaraible('acc.z', 'float'),
    ]
    loggers.append(FileLogger(logconf, 'acc.csv', logvars))

    logconf = LogConfig(name='ActiveMarker', period_in_ms=100)
    logvars = [
        LogVaraible('activeMarker.btSns', 'uint8_t'),
        LogVaraible('activeMarker.i2cOk', 'uint8_t'),
    ]
    loggers.append(FileLogger(logconf, 'activeMarker.csv', logvars))

    logconf = LogConfig(name='Baro', period_in_ms=100)
    logvars = [
        LogVaraible('baro.pressure', 'float'),
        LogVaraible('baro.asl', 'float'),
        LogVaraible('baro.temp', 'float'),
    ]
    loggers.append(FileLogger(logconf, 'baro.csv', logvars))

    logconf = LogConfig(name='Controller1', period_in_ms=100)
    logvars = [
        LogVaraible('controller.accelz', 'float'),
        LogVaraible('controller.actuatorThrust', 'float'),
        LogVaraible('controller.cmd_pitch', 'float'),
        LogVaraible('controller.cmd_roll', 'float'),
        LogVaraible('controller.cmd_thrust', 'float'),
        LogVaraible('controller.cmd_yaw', 'float'),
    ]
    loggers.append(FileLogger(logconf, 'controller1.csv', logvars))

    logconf = LogConfig(name='Controller2', period_in_ms=100)
    logvars = [
        LogVaraible('controller.ctr_yaw', 'int16_t'),
        LogVaraible('controller.pitch', 'float'),
        LogVaraible('controller.pitchRate', 'float'),
        LogVaraible('controller.r_pitch', 'float'),
        LogVaraible('controller.r_roll', 'float'),
        LogVaraible('controller.r_yaw', 'float'),
    ]
    loggers.append(FileLogger(logconf, 'controller2.csv', logvars))

    logconf = LogConfig(name='Controller3', period_in_ms=100)
    logvars = [
        LogVaraible('controller.roll', 'int16_t'),
        LogVaraible('controller.rollRate', 'float'),
        LogVaraible('controller.yaw', 'float'),
        LogVaraible('controller.yawRate', 'float'),
    ]
    loggers.append(FileLogger(logconf, 'controller3.csv', logvars))

    logconf = LogConfig(name='ctrltarget1', period_in_ms=100)
    logvars = [
        LogVaraible('ctrltarget.x', 'float'),
        LogVaraible('ctrltarget.y', 'float'),
        LogVaraible('ctrltarget.z', 'float'),
        LogVaraible('ctrltarget.vx', 'float'),
        LogVaraible('ctrltarget.vx', 'float'),
        LogVaraible('ctrltarget.vx', 'float'),
    ]
    loggers.append(FileLogger(logconf, 'ctrltarget1.csv', logvars))

    logconf = LogConfig(name='ctrltarget2', period_in_ms=100)
    logvars = [
        LogVaraible('ctrltarget.ax', 'float'),
        LogVaraible('ctrltarget.ay', 'float'),
        LogVaraible('ctrltarget.az', 'float'),
        LogVaraible('ctrltarget.roll', 'float'),
        LogVaraible('ctrltarget.pitch', 'float'),
        LogVaraible('ctrltarget.yaw', 'float'),
    ]
    loggers.append(FileLogger(logconf, 'ctrltarget2.csv', logvars))

    logconf = LogConfig(name='ctrltargetZ1', period_in_ms=100)
    logvars = [
        LogVaraible('ctrltargetZ.x', 'int16_t'),
        LogVaraible('ctrltargetZ.y', 'int16_t'),
        LogVaraible('ctrltargetZ.z', 'int16_t'),
        LogVaraible('ctrltargetZ.vx', 'int16_t'),
        LogVaraible('ctrltargetZ.vy', 'int16_t'),
        LogVaraible('ctrltargetZ.vz', 'int16_t'),
    ]
    loggers.append(FileLogger(logconf, 'ctrltargetZ1.csv', logvars))

    logconf = LogConfig(name='ctrltargetZ2', period_in_ms=100)
    logvars = [
        LogVaraible('ctrltargetZ.ax', 'int16_t'),
        LogVaraible('ctrltargetZ.ay', 'int16_t'),
        LogVaraible('ctrltargetZ.az', 'int16_t'),
    ]
    loggers.append(FileLogger(logconf, 'ctrltargetZ2.csv', logvars))

    logconf = LogConfig(name='extrx', period_in_ms=100)
    logvars = [
        LogVaraible('extrx.AltHold', 'uint8_t'),
        LogVaraible('extrx.Arm', 'uint8_t'),
        LogVaraible('extrx.thrust', 'float'),
        LogVaraible('extrx.roll', 'float'),
        LogVaraible('extrx.pitch', 'float'),
        LogVaraible('extrx.yawRate', 'float'),
        LogVaraible('extrx.zVel', 'float'),
    ]
    loggers.append(FileLogger(logconf, 'extrx.csv', logvars))

    logconf = LogConfig(name='extrx_raw', period_in_ms=100)
    logvars = [
        LogVaraible('extrx_raw.ch0', 'uint16_t'),
        LogVaraible('extrx.Arm', 'uint8_t'),
        LogVaraible('extrx.thrust', 'float'),
        LogVaraible('extrx.roll', 'float'),
        LogVaraible('extrx.pitch', 'float'),
        LogVaraible('extrx.yawRate', 'float'),
        LogVaraible('extrx.zVel', 'float'),
    ]
    loggers.append(FileLogger(logconf, 'extrx_raw.csv', logvars))
    
    logconf = LogConfig(name='Position', period_in_ms=100)
    logvars = [
        LogVaraible('stateEstimate.x', 'float'),
        LogVaraible('stateEstimate.y', 'float'),
        LogVaraible('stateEstimate.z', 'float'),
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

    logconf = LogConfig(name='range', period_in_ms=100)
    logvars = [
        LogVaraible('range.zrange', 'float'),
    ]
    loggers.append(FileLogger(logconf, 'range.csv', logvars))

    # logconf = LogConfig(name='target', period_in_ms=100)
    # logvars = [
    #     LogVaraible('ctrltarget.ax', 'float'),
    #     LogVaraible('ctrltarget.ay', 'float'),
    #     LogVaraible('ctrltarget.az', 'float'),
    #     LogVaraible('ctrltarget.vx', 'float'),
    #     LogVaraible('ctrltarget.vy', 'float'),
    #     LogVaraible('ctrltarget.vz', 'float'),
    # ]
    # loggers.append(FileLogger(logconf, 'target.csv', logvars))

    # logconf = LogConfig(name='sys', period_in_ms=100)
    # logvars = [
    #     LogVaraible('sys.armed', 'int8_t'),
    #     LogVaraible('sys.canfly', 'uint8_t'),
    #     LogVaraible('sys.isFlying', 'uint8_t'),
    #     LogVaraible('sys.isTumbled', 'uint8_t'),
    # ]
    # loggers.append(FileLogger(logconf, 'sys.csv', logvars))

    # logconf = LogConfig(name='tdoaEngine', period_in_ms=100)
    # logvars = [
    #     LogVaraible('tdoaEngine.stRx', 'float'),
    #     LogVaraible('tdoaEngine.stEst', 'float'),
    #     LogVaraible('tdoaEngine.stTime', 'float'),
    #     LogVaraible('tdoaEngine.stFound', 'float'),
    #     LogVaraible('tdoaEngine.stCc', 'float'),
    #     LogVaraible('tdoaEngine.stHit', 'float'),
    #     LogVaraible('tdoaEngine.tof', 'uint16_t'),
    # ]
    # loggers.append(FileLogger(logconf, 'tdoaEngine.csv', logvars))

    # logconf = LogConfig(name='radio', period_in_ms=100)
    # logvars = [
    #     LogVaraible('radio.rssi', 'int8_t'),
    #     LogVaraible('radio.isConnected', 'int8_t'),

    # ]
    # loggers.append(FileLogger(logconf, 'radio.csv', logvars))

    # logconf = LogConfig(name='posCtl', period_in_ms=100)
    # logvars = [
    #     LogVaraible('posCtl.targetVX', 'float'),
    #     LogVaraible('posCtl.targetVY', 'float'),
    #     LogVaraible('posCtl.targetVZ', 'float'),
    #     LogVaraible('posCtl.targetX', 'float'),
    #     LogVaraible('posCtl.targetY', 'float'),
    #     LogVaraible('posCtl.targetZ', 'float'),

    # ]
    # loggers.append(FileLogger(logconf, 'posCtl.csv', logvars))

    # logconf = LogConfig(name='posCtl1', period_in_ms=100)
    # logvars = [
    #     LogVaraible('posCtl.bodyVX', 'float'),
    #     LogVaraible('posCtl.bodyVY', 'float'),
    #     LogVaraible('posCtl.bodyX', 'float'),
    #     LogVaraible('posCtl.bodyY', 'float'),
    #     LogVaraible('posCtl.Yp', 'float'),
    #     LogVaraible('posCtl.Yi', 'float'),

    # ]
    # loggers.append(FileLogger(logconf, 'posCtl1.csv', logvars))

    # logconf = LogConfig(name='posCtl2', period_in_ms=100)
    # logvars = [
    #     LogVaraible('posCtl.Yd', 'float'),
    #     LogVaraible('posCtl.Zp', 'float'),
    #     LogVaraible('posCtl.Zi', 'float'),
    #     LogVaraible('posCtl.Zd', 'float'),

    # ]
    # loggers.append(FileLogger(logconf, 'posCtl2.csv', logvars))

    # logconf = LogConfig(name='posCtl3', period_in_ms=100)
    # logvars = [
    #     LogVaraible('posCtl.VXp', 'float'),
    #     LogVaraible('posCtl.VXi', 'float'),
    #     LogVaraible('posCtl.VXd', 'float'),
    #     LogVaraible('posCtl.VZp', 'float'),
    #     LogVaraible('posCtl.VZi', 'float'),
    #     LogVaraible('posCtl.VZd', 'float'),

    # ]
    # loggers.append(FileLogger(logconf, 'posCtl3.csv', logvars))


    # logconf = LogConfig(name='posCtrlIndi', period_in_ms=100)
    # logvars = [
    #     LogVaraible('posCtrlIndi.posRef_x', 'float'),
    #     LogVaraible('posCtrlIndi.posRef_y', 'float'),
    #     LogVaraible('posCtrlIndi.posRef_z', 'float'),
    #     LogVaraible('posCtrlIndi.velS_x', 'float'),
    #     LogVaraible('posCtrlIndi.velS_y', 'float'),
    #     LogVaraible('posCtrlIndi.velS_z', 'float'),

    # ]
    # loggers.append(FileLogger(logconf, 'posCtrlIndi.csv', logvars))

    # logconf = LogConfig(name='posCtrlIndi1', period_in_ms=100)
    # logvars = [
    #     LogVaraible('posCtrlIndi.velRef_x', 'float'),
    #     LogVaraible('posCtrlIndi.velRef_y', 'float'),
    #     LogVaraible('posCtrlIndi.velRef_z', 'float'),
    #     LogVaraible('posCtrlIndi.angS_roll', 'float'),
    #     LogVaraible('posCtrlIndi.angS_pitch', 'float'),
    #     LogVaraible('posCtrlIndi.angS_yaw', 'float'),

    # ]
    # loggers.append(FileLogger(logconf, 'posCtrlIndi1.csv', logvars))

    # logconf = LogConfig(name='posCtrlIndi2', period_in_ms=100)
    # logvars = [
    #     LogVaraible('posCtrlIndi.angS_yaw', 'float'),
    #     LogVaraible('posCtrlIndi.angF_roll', 'float'),
    #     LogVaraible('posCtrlIndi.angF_pitch', 'float'),
    #     LogVaraible('posCtrlIndi.angF_yaw', 'float'),
    #     LogVaraible('posCtrlIndi.accRef_x', 'float'),
    #     LogVaraible('posCtrlIndi.accRef_y', 'float'),

    # ]
    # loggers.append(FileLogger(logconf, 'posCtrlIndi2.csv', logvars))

    return loggers

def start_logging(cf, loggers):
    for logger in loggers:
        logger.start(cf)    

def stop_logging(loggers):
    for logger in loggers:
        logger.stop() 

if __name__ == '__main__':
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

        time.sleep(1)
        stop_logging(loggers)
    