# -*- coding: utf-8 -*-
#

import logging
import time
import os
import numpy as np
import argparse

import cflib.crtp
from cflib.crazyflie.log import LogConfig
from cflib.crazyflie.syncCrazyflie import SyncCrazyflie
from cflib.crazyflie.syncLogger import SyncLogger
from cflib.utils.power_switch import PowerSwitch
from cflib.positioning.position_hl_commander import PositionHlCommander

# URI = 'radio://0/80/2M/E7E7E7E7E7'
#URI = 'radio://0/80/2M/E7E7E7E7E8'
URI = 'radio://0/80/2M/E7E7E7E7E9'

INTENSITY = 100
usdCanLog = 1
deckFlow2 = 0

def consoleReceived(data):
    print(data, end='')

def paramReceived(name, value):
    global usdCanLog
    global deckFlow2
    if name == "usd.canLog":
        usdCanLog = int(value)
    if name == "deck.bcFlow2":
        deckFlow2 = int(value)


if __name__ == '__main__':
    # Only output errors from the logging framework
    logging.basicConfig(level=logging.ERROR)

    # Initialize the low-level drivers (don't list the debug drivers)
    cflib.crtp.init_drivers(enable_debug_driver=False)

    s = PowerSwitch(URI)
    s.stm_power_cycle()
    s.close()
    time.sleep(5)

    lg = LogConfig(name='Battery', period_in_ms=10)
    lg.add_variable('pm.vbat', 'float')
    lg.add_variable('lighthouse.status', 'uint8_t')

    cf = cflib.crazyflie.Crazyflie()
    cf.console.receivedChar.add_callback(consoleReceived)

    with SyncCrazyflie(URI, cf) as scf:

        # check usd Deck
        cf.param.add_update_callback(group='usd', name='canLog', cb=paramReceived)
        cf.param.request_param_update('usd.canLog')

        # check flow deck
        cf.param.add_update_callback(group='deck', name='bcFlow2', cb=paramReceived)
        cf.param.request_param_update('deck.bcFlow2')

        # check battery voltage
        with SyncLogger(scf, lg) as logger:
            for _, data, _ in logger:
                vbat = data['pm.vbat']
                lhStatus = data['lighthouse.status']
                break

        print("Battery voltage: {:.2f} V".format(vbat))
        print("LightHouse Status: {}".format(lhStatus))

        if vbat < 3.6:
            exit("Battery too low!")

        if lhStatus != 2 and deckFlow2 != 1:
            exit("LightHouse not working or flow not available!")

        if usdCanLog != 1:
            exit("Can't log to USD!")

        # start logging in uSD card
        cf.param.set_value('usd.logging', 1)
        time.sleep(2)

        with PositionHlCommander(scf, default_height=0.5, controller=PositionHlCommander.CONTROLLER_PID) as pc:
            pc.go_to( x=0.0, y=0.0, velocity=0.3)
            pc.go_to( x=2.0, y=0.0, velocity=0.3)
            pc.land()
            time.sleep(5)
            pc.take_off( height=0.5, velocity=0.3)
            pc.go_to( x=0.0, y=0.0, velocity=0.3)
            pc.land()

        # stop logging in uSD card
        cf.param.set_value('usd.logging', 0)
        time.sleep(2)

    # Turn CF off
    s = PowerSwitch(URI)
    s.stm_power_down()
    s.close()