# MicroPython Script for ESP32
# Author: Himanshu Tripathi

# buzzer interfacing with esp32

import machine
import time

# object for pin
p23 = machine.Pin(23,machine.Pin.OUT)

# pwm object
buzzer = machine.PWM(p23)
# https://www.engineeringtoolbox.com/note-frequencies-d_520.html
# user may select the frequency as per the note and octave 
buzzer.freq(1109)
buzzer.duty(50)
time.sleep(0.5)
buzzer.duty(0)
# deinit the pin from pwm
# this pin will work as normal output pin 
buzzer.deinit()