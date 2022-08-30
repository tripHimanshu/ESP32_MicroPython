# MicroPython script for ESP32
# Author: Himanshu Tripathi

# Timers  in ESP32 
# ESP32 port has four hardware timers
# with Timer ID 0 to 3

from machine import Pin, Timer

# object for led
led = Pin(2,Pin.OUT)

# object for Timer 0
timer0 = Timer(0)
# timer function
timer0.init(period=1000,mode=Timer.PERIODIC,callback=lambda t: led.value(not led.value()))

# callback function for timer1
def timer1_func(t):
    print('LED is on' if led.value() else 'LED is off')
    
# object for timer 1
timer1 = Timer(1)
# timer function
timer1.init(period=1001,mode=Timer.PERIODIC,callback=timer1_func)




while True:
    pass
        
