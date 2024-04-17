# General information
Scripts for plotting graphs based on logs collected in binary form:
1. decrypt_controller_data.py
2. decrypt_motor_data.py

Collecting logs during the flight onto a microSD card; the list of parameters is specified in the config.txt file.

# List of logged parameters decrypted by the script

## Script decrypt_controller_data.py
- stateEstimate.x Estimated position of the platform in the global reference system, X [m].
- stateEstimate.y Estimated position of the platform in the global reference system, Y [m].
- stateEstimate.z Estimated position of the platform in the global reference system, Z [m].
- controller.cmd_roll Roll command.
- controller.cmd_pitch Pitch command.
- controller.cmd_yaw Yaw command.
- controller.r_roll Roll measurement by gyroscope in radians.
- controller.r_pitch Pitch measurement by the gyroscope in radians.
- controller.r_yaw Yaw measurement in radians.
- controller.accelz Acceleration along the z axis in G-force.
- controller.actuatorThrust Thrust command without compensation (tilt).
- controller.roll Desired roll setpoint.
- controller.pitch Desired pitch reference value.
- controller.yaw Desired yaw setpoint.
- controller.rollRate Desired roll rate setpoint.
- controller.pitchRate Desired pitch rate setpoint.
- controller.yawRate Desired yaw rate setpoint.
- controller.ctr_yaw Something with yaw.

## Script decrypt_motor_data.py
- motor.m1 Motor power M1
- motor.m2 Motor power M2
- motor.m3 Motor power M3
- motor.m4 Motor power M4
- pwm.m1_pwm PWM output current for motor M1
- pwm.m2_pwm PWM output current for motor M2
- pwm.m3_pwm PWM output current for motor M3
- pwm.m4_pwm PWM output current for motor M4
- pm.vbatMV Battery charge (mV)
- stateEstimate.x Estimated position of the platform in the global reference system, X [m].
- stateEstimate.y Estimated position of the platform in the global reference system, Y [m].
- stateEstimate.z Estimated position of the platform in the global reference system, Z [m].
- stateEstimate.vx Crazyflie speed in global reference frame, X [m/s].
- stateEstimate.vy Speed of Crazyflie in the global reference frame, Y [m/s].
- stateEstimate.vz Speed of Crazyflie in the global reference frame, Z [m/s].
- stateEstimate.ax Crazyflie acceleration in global reference frame, X [Gs].
- stateEstimate.ay Crazyflie acceleration in global reference frame, Y [Gs].
- stateEstimate.az Acceleration of Crazyflie in the global reference frame, excluding gravity, Z [Gs].
- stateEstimate.roll Position in space, roll angle [degree].
- stateEstimate.yaw Position in space, yaw angle [degree].

# Run script
As a script argument, the path to the file containing the flight log is passed.
 
Example of running a script:
    
     python3 ./src/decrypt_data/decrypt_controller_data.py "./data/controller_data/add_weight_W1_near_M3_M4/E8_log00"
