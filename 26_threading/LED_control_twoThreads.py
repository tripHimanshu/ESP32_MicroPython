# MicroPython Script for ESP32
# Author: Himanshu Tripathi

# controlling led on and off using threads
# one thread turn on the led, while
# the second thread turn off the led 

import machine 
import _thread
import time

# led object
led = machine.Pin(2,machine.Pin.OUT)

# global variable
toggle = False

# clock for synchronization between two threads
lock = _thread.allocate_lock()

# led_on and led_off functions are just for demonstration purpose
# to show that how we may call any function inside a thread
# function for led on
def led_on():
    led.value(1)
# function for led off
def led_off():
    led.value(0)

# function for the thread
# this function turns off the led 
def switch_off():
    global toggle
    while True:
        lock.acquire()
        if toggle:
            led_off()
            toggle = False
        time.sleep(1)
        lock.release()
# start the thread
_thread.start_new_thread(switch_off,())

# another thread to turn on the led 
while True:
    lock.acquire()
    toggle = True
    led_on()
    time.sleep(1)
    lock.release()
