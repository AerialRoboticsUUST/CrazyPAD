# Общие сведения
Скрипты построения графиков по логам, собранным в бинарном виде:
1. decrypt_controller_data.py
2. decrypt_motor_data.py

Сборка логов в ходе полета на карту microSD, перечень параметров задается в файле config.txt.

# Перечень логируемых параметров, расшифровываемых скриптом

## Скриптом decrypt_controller_data.py
- stateEstimate.x  Расчетное положение платформы в глобальной системе отсчета, X [м].
- stateEstimate.y  Расчетное положение платформы в глобальной системе отсчета, Y [м].
- stateEstimate.z  Предполагаемое положение платформы в глобальной системе отсчета, Z [м].
- controller.cmd_roll  Команда вращения.
- controller.cmd_pitch Команда шага.
- controller.cmd_yaw  команда рыскания
- controller.r_roll Измерение крена гироскопа в радианах.
- controller.r_pitch  Измерение шага гироскопа в радианах.
- controller.r_yaw  Измерение рысканья в радианах.
- controller.accelz  Ускорение по оси z в G-force.
- controller.actuatorThrust  Команда тяги без компенсации (наклона).
- controller.roll  Желаемая уставка вращения.
- controller.pitch  Желаемая уставка шага.
- controller.yaw  Желаемая уставка рыскания.
- controller.rollRate  Требуемая уставка скорости вращения.
- controller.pitchRate  Желаемая уставка скорости тангажа.
- controller.yawRate  Требуемая уставка скорости рыскания.
- controller.ctr_yaw Что-то с рысканьем.

## Скриптом decrypt_motor_data.py
- motor.m1	Мощность мотора М1
- motor.m2	Мощность мотора М2
- motor.m3	Мощность мотора М3
- motor.m4    Мощность мотора М4
- pwm.m1_pwm	 	Сила тока ШИМ на выходе для мотора М1
- pwm.m2_pwm	 	Сила тока ШИМ на выходе для мотора М2
- pwm.m3_pwm	 	Сила тока ШИМ на выходе для мотора М3
- pwm.m4_pwm      Сила тока ШИМ на выходе для мотора М4
- pm.vbatMV   Заряд батареи (mV)
- stateEstimate.x  Расчетное положение платформы в глобальной системе отсчета, X [м].
- stateEstimate.y  Расчетное положение платформы в глобальной системе отсчета, Y [м].
- stateEstimate.z  Предполагаемое положение платформы в глобальной системе отсчета, Z [м].
- stateEstimate.vx Скорость Crazyflie в глобальной системе отсчета, X [м/с].
- stateEstimate.vy Скорость Crazyflie в глобальной системе отсчета, Y [м/с].
- stateEstimate.vz Скорость Crazyflie в глобальной системе отсчета, Z [м/с].
- stateEstimate.ax Ускорение Crazyflie в глобальной системе отсчета, X [Gs].
- stateEstimate.ay Ускорение Crazyflie в глобальной системе отсчета, Y [Gs].
- stateEstimate.az Ускорение Crazyflie в глобальной системе отсчета, без учета гравитации, Z [Gs].
- stateEstimate.roll Положение, угол крена [градус].
- stateEstimate.yaw Отношение, угол рыскания [градус].

# Запуск скрипт
В качестве аргумента скрипта, передается путь к файлу, содержащему лог полета.
 
Пример запуска скрипта:
    
    python3 ./src/decrypt_data/decrypt_controller_data.py "./data/controller_data/add_weght_W1_near_M3_M4/E8_log00"
