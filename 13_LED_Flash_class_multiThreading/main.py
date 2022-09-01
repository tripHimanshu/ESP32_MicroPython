# MicroPython Script for ESP32
# Author: Himanshu Tripathi

# LED blinking with non-blocking delay

import machine
import time

class Flash_led:
    def __init__(self,pin,on_time,off_time):
        self.pin = pin
        self.on_time = on_time
        self.off_time = off_time
        self.last_change = time.ticks_ms()
        self.led_state = 0
        self.led = machine.Pin(self.pin,machine.Pin.OUT)
    def flashing(self):
        if ((self.led_state is 1) and ((time.ticks_ms()-self.last_change)>self.on_time)):
            self.last_change = time.ticks_ms()
            self.led_state = 0
            self.led.value(self.led_state)
            print('LED is off')
        elif ((self.led_state is 0) and ((time.ticks_ms()-self.last_change)>self.off_time)):
            self.last_change = time.ticks_ms()
            self.led_state = 1
            self.led.value(self.led_state)
            print('LED is on')

# object for Flash_led class
led1 = Flash_led(2,500,1000)
while True:
    Flash_led.flashing(led1)
            
        
