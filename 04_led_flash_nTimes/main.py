# MicroPython script for ESP32
# Author: Himanshu Tripathi

# define function for led flashing for n number of times

from machine import Pin
from time import sleep

# create object for led
led = Pin(2,Pin.OUT)
# create object for button
button = Pin(0,Pin.IN)

# function for led flash
def flash_led_nTimes(number,onTime,offTime,msg):
    counter = 0
    while counter < number:
        led.on()
        sleep(onTime)
        led.off()
        sleep(offTime)
        counter += 1
    print(msg)
    
while True:
    if not button.value():
        flash_led_nTimes(3,0.3,0.5,'Flashing Done')
        