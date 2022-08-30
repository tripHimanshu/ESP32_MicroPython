# MicroPython script for ESP32
# Author: Himanshu Tripathi

# ESP32 PWM
# LED fading using PWM
# PWM can be enabled on all output enable pins
# the base frequency can range from 1 Hz to 40 MHz
# but there is a trade-off
# as the base frequency increases, the duty resolution decreases

from machine import Pin, Timer, PWM
from time import sleep_ms

# pwm object and its configuration
# PWM frequency = 1000 Hz 
pwm2 = PWM(Pin(2),freq=1000)

while True:
#     increase the LED brightness
    print('Increasing LED brightness..')
    for i in range (0,1024):
        pwm2.duty(i)
        sleep_ms(2)
        i += 1
    print('LED is at its max brightness')
        
#     wait at max brightness for 2 sec
    sleep_ms(2000)

#     decrease the LED brightness
    print('Decrasing LED brightness..')
    for i in range (0,1024):
        pwm2.duty(1023-i)
        sleep_ms(2)
        i += 1
    print('LED is at its min brightness')
#     wait at min brightness for 2 sec
    sleep_ms(2000)