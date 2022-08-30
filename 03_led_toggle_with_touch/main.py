# MicroPython script for ESP32
# Author: Himanshu Tripathi

# toggle the state of led with touch on a Pin

from machine import Pin, TouchPad

# create object for led pin
led = Pin(2, Pin.OUT)
# create object for touch pin
touch = TouchPad(Pin(4))

# run forever
while True:
    # read the value of touch pin 
    if touch.read() < 400:
        led.value(not led.value())
        print("LED turned on" if led.value() else "LED turned off")
        # wait till the pin is touched
        while touch.read() < 400:
            pass

