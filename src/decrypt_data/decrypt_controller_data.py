# -*- coding: utf-8 -*-
"""
plotting controller data log
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

plotRows = 8

plotCurrent += 1
plt.subplot(plotRows, plotCols, plotCurrent)
plt.plot(logData['timestamp'], logData['controller.accelz'], '-')
plt.xlabel('timestamp [ms]')
plt.ylabel('controller.accelz')

plotCurrent += 1
plt.subplot(plotRows, plotCols, plotCurrent)
plt.plot(logData['timestamp'], logData['controller.actuatorThrust'], '-')
plt.xlabel('timestamp [ms]')
plt.ylabel('controller.actuatorThrust')

plotCurrent += 1
plt.subplot(plotRows, plotCols, plotCurrent)
plt.plot(logData['timestamp'], logData['controller.ctr_yaw'], '-')
plt.xlabel('timestamp [ms]')
plt.ylabel('controller.ctr_yaw')

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
plt.plot(logData['timestamp'], logData['controller.cmd_thrust'], '-', label='cmd_thrust')
plt.plot(logData['timestamp'], logData['controller.cmd_roll'], '-', label='cmd_roll')
plt.plot(logData['timestamp'], logData['controller.cmd_pitch'], '-', label='cmd_pitch')
plt.plot(logData['timestamp'], logData['controller.cmd_yaw'], '-', label='cmd_yaw')
plt.xlabel('timestamp [ms]')
plt.ylabel('Controller cmd')
plt.legend(loc=9, ncol=3, borderaxespad=0.)

plotCurrent += 1
plt.subplot(plotRows, plotCols, plotCurrent)
plt.plot(logData['timestamp'], logData['controller.r_roll'], '-', label='r_roll')
plt.plot(logData['timestamp'], logData['controller.r_pitch'], '-', label='r_pitch')
plt.plot(logData['timestamp'], logData['controller.r_yaw'], '-', label='r_yaw')
plt.xlabel('timestamp [ms]')
plt.ylabel('Controller r')
plt.legend(loc=9, ncol=3, borderaxespad=0.)

plotCurrent += 1
plt.subplot(plotRows, plotCols, plotCurrent)
plt.plot(logData['timestamp'], logData['controller.roll'], '-', label='roll')
plt.plot(logData['timestamp'], logData['controller.pitch'], '-', label='pitch')
plt.plot(logData['timestamp'], logData['controller.yaw'], '-', label='yaw')
plt.xlabel('timestamp [ms]')
plt.ylabel('Controller')
plt.legend(loc=9, ncol=3, borderaxespad=0.)

plotCurrent += 1
plt.subplot(plotRows, plotCols, plotCurrent)
plt.plot(logData['timestamp'], logData['controller.rollRate'], '-', label='rollRate')
plt.plot(logData['timestamp'], logData['controller.pitchRate'], '-', label='pitchRate')
plt.plot(logData['timestamp'], logData['controller.yawRate'], '-', label='yawRate')
plt.xlabel('timestamp [ms]')
plt.ylabel('Controller rate')
plt.legend(loc=9, ncol=3, borderaxespad=0.)

plt.show()