# -*- coding: utf-8 -*-
"""
plotting a motor data log
"""
import cfusdlog
import matplotlib.pyplot as plt
import re
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("filename")
args = parser.parse_args()

# decode binary log data
logData = cfusdlog.decode(args.filename)

#only focus on regular logging
logData = logData['fixedFrequency']

# set window background to white
plt.rcParams['figure.facecolor'] = 'w'
    
# number of columns and rows for suplot
plotCols = 1
plotRows = 1

# let's see which keys exists in current data set
keys = ""
for k, v in logData.items():
    keys += k
    
# current plot for simple subplot usage
plotCurrent = 0

# new figure
plt.figure(0)

plotRows = 7

plotCurrent += 1
plt.subplot(plotRows, plotCols, plotCurrent)
plt.plot(logData['timestamp'], logData['pm.vbatMV'], '-')
plt.xlabel('timestamp [ms]')
plt.ylabel('Battery charge [mV]')

plotCurrent += 1
plt.subplot(plotRows, plotCols, plotCurrent)
plt.plot(logData['timestamp'], logData['stateEstimate.roll'], '-', label='roll')
plt.plot(logData['timestamp'], logData['stateEstimate.yaw'], '-', label='yaw')
plt.xlabel('timestamp [ms]')
plt.ylabel('Stabilizer')
plt.legend(loc=9, ncol=4, borderaxespad=0.)

plotCurrent += 1
plt.subplot(plotRows, plotCols, plotCurrent)
plt.plot(logData['timestamp'], logData['stateEstimate.x'], '-', label='X')
plt.plot(logData['timestamp'], logData['stateEstimate.y'], '-', label='Y')
plt.plot(logData['timestamp'], logData['stateEstimate.z'], '-', label='Z')
plt.xlabel('timestamp [ms]')
plt.ylabel('Coordinate [m]')
plt.legend(loc=9, ncol=3, borderaxespad=0.)

plotCurrent += 1
plt.subplot(plotRows, plotCols, plotCurrent)
plt.plot(logData['timestamp'], logData['stateEstimate.vx'], '-', label='VX')
plt.plot(logData['timestamp'], logData['stateEstimate.vy'], '-', label='VY')
plt.plot(logData['timestamp'], logData['stateEstimate.vz'], '-', label='VZ')
plt.xlabel('timestamp [ms]')
plt.ylabel('Speed [m/s]')
plt.legend(loc=9, ncol=3, borderaxespad=0.)

plotCurrent += 1
plt.subplot(plotRows, plotCols, plotCurrent)
plt.plot(logData['timestamp'], logData['stateEstimate.ax'], '-', label='AX')
plt.plot(logData['timestamp'], logData['stateEstimate.ay'], '-', label='AY')
plt.plot(logData['timestamp'], logData['stateEstimate.az'], '-', label='AZ')
plt.xlabel('timestamp [ms]')
plt.ylabel('Acceleration [m/s^2]')
plt.legend(loc=9, ncol=3, borderaxespad=0.)

plotCurrent += 1
plt.subplot(plotRows, plotCols, plotCurrent)
plt.plot(logData['timestamp'], logData['motor.m1'], '-', label='m1')
plt.plot(logData['timestamp'], logData['motor.m2'], '-', label='m2')
plt.plot(logData['timestamp'], logData['motor.m3'], '-', label='m3')
plt.plot(logData['timestamp'], logData['motor.m4'], '-', label='m4')

plt.xlabel('timestamp [ms]')
plt.ylabel('Motor')
plt.legend(loc=9, ncol=4, borderaxespad=0.)


plotCurrent += 1
plt.subplot(plotRows, plotCols, plotCurrent)
plt.plot(logData['timestamp'], logData['pwm.m1_pwm'], '-', label='m1_pwm')
plt.plot(logData['timestamp'], logData['pwm.m2_pwm'], '-', label='m2_pwm')
plt.plot(logData['timestamp'], logData['pwm.m3_pwm'], '-', label='m3_pwm')
plt.plot(logData['timestamp'], logData['pwm.m4_pwm'], '-', label='m4_pwm')
plt.xlabel('timestamp [ms]')
plt.ylabel('PWM')
plt.legend(loc=9, ncol=4, borderaxespad=0.)

plt.show()