# Общие сведения
Скрипты построения графиков по логам, собранным в бинарном виде:
1. decrypt_controller_data.py
2. decrypt_motor_data.py

Сборка логов в ходе полета на карту microSD, перечень параметров задается в файле config.txt.

# Перечень логируемых параметров, расшифровываемых скриптом

## Скриптом decrypt_controller_data.py
- stateEstimate.x  Расчетное положение платформы в глобальной системе отсчета, X [м].
- stateEstimate.y  Расчетное положение платформы в глобальной системе отсчета, Y [м].
- stateEstimate.z  Расчетное положение платформы в глобальной системе отсчета, Z [м].
- controller.cmd_roll  Команда крена.
- controller.cmd_pitch Команда тангажа.
- controller.cmd_yaw  Команда рыскания
- controller.r_roll Измерение крена гироскопа в радианах.
- controller.r_pitch  Измерение тангажа гироскопа в радианах.
- controller.r_yaw  Измерение рысканья в радианах.
- controller.accelz  Ускорение по оси z в G-force.
- controller.actuatorThrust  Команда тяги без компенсации (наклона).
- controller.roll  Желаемое заданное значение крена.
- controller.pitch  Желаемое заданное значение тангажа.
- controller.yaw  Желаемое заданное значение рыскания.
- controller.rollRate  Желаемое заданное значение скорости крена.
- controller.pitchRate  Желаемое заданное значение тангажа.
- controller.yawRate  Желаемое заданное значение скорости рыскания.
- controller.ctr_yaw Что-то с рысканьем.

## Скриптом decrypt_motor_data.py
- motor.m1	Мощность мотора М1
- motor.m2	Мощность мотора М2
- motor.m3	Мощность мотора М3
- motor.m4    Мощность мотора М4
- pwm.m1_pwm	 	Сила тока ШИМ на выходе для мотора М1
- pwm.m2_pwm	 	Сила тока ШИМ на выходе для мотора М2
- pwm.m3_pwm	 	Сила тока ШИМ на выходе для мотора М3
- pwm.m4_pwm   Сила тока ШИМ на выходе для мотора М4
- pm.vbatMV   Заряд батареи (mV)
- stateEstimate.x  Расчетное положение платформы в глобальной системе отсчета, X [м].
- stateEstimate.y  Расчетное положение платформы в глобальной системе отсчета, Y [м].
- stateEstimate.z  Расчетное положение платформы в глобальной системе отсчета, Z [м].
- stateEstimate.vx Скорость Crazyflie в глобальной системе отсчета, X [м/с].
- stateEstimate.vy Скорость Crazyflie в глобальной системе отсчета, Y [м/с].
- stateEstimate.vz Скорость Crazyflie в глобальной системе отсчета, Z [м/с].
- stateEstimate.ax Ускорение Crazyflie в глобальной системе отсчета, X [Gs].
- stateEstimate.ay Ускорение Crazyflie в глобальной системе отсчета, Y [Gs].
- stateEstimate.az Ускорение Crazyflie в глобальной системе отсчета, без учета гравитации, Z [Gs].
- stateEstimate.roll Положение в пространстве, угол крена [градус].
- stateEstimate.yaw  Положение в пространстве, угол рыскания [градус].

# Запуск скрипта
В качестве аргумента скрипта, передается путь к файлу, содержащему лог полета.
 
Пример запуска скрипта:
    
    python3 ./src/decrypt_data/decrypt_controller_data.py "./data/controller_data/add_weight_W1_near_M3_M4/E8_log00"
