# MicroPython Script for ESP32
# Author: Himanshu Tripathi

# LED blinking with non-blocking delay

import machine
import time

# object for led pin
led = machine.Pin(2,machine.Pin.OUT)

# global variable
start_time = time.ticks_ms()
interval = 500 # time in ms 

# blink the LED forever
while True:
    if (time.ticks_ms()-start_time) >= interval:
        start_time = time.ticks_ms()
        led.value(not led.value())
        print('LED is on' if (led.value()) else 'LED is off')
        
