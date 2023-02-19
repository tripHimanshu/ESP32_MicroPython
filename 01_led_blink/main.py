# MicroPython script for ESP32
# Author: Himanshu Tripathi

# blink the led and print led state on terminal

from machine import Pin
from time import sleep

# create object for led pin
led = Pin(2,Pin.OUT)

# global variable
led_state = True

# blink the led forever
# print the state of led on terminal
while True:
    led_state = not led_state
    led.value(led_state)
    print("LED turned on" if led_state else "LED turned off")
    # wait for some time
    sleep(2)