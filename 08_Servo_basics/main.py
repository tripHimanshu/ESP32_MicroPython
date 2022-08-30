# MicroPython script for ESP32
# Author: Himanshu Tripathi

# servo motor drive usign ESP32
# frequency = 1 / Period = 1 / 20 ms = 50 Hz
# Duty Cycle (1 ms) = 1 / 20 ms = 0.05 => 5%
# Duty Cycle (2 ms) = 2 / 20 ms = 0.10 => 10%
# Duty Cycle value
# 0.05 * 1024 = 51.2
# 0.10 * 1024 = 102.4

import machine
import time

# PWM pin object
pwm = machine.PWM(machine.Pin(13),freq=50)

# map function for MicroPython
def map(x,in_min,in_max,out_min,out_max):
    return int((x-in_min)*(out_max-out_min) / (in_max-in_min) + out_min)

# set servo at 0 position 
pwm.duty(map(0,0,180,18,140))

# rotate servo from 0 to 180
for i in range (0,181,10):
    pwm.duty(map(i,0,180,18,140))
    time.sleep(0.5)

# rotate servo from 180 to 0
for i in range (180,-1,-10):
    pwm.duty(map(i,0,180,18,140))
    time.sleep(0.5)

 
