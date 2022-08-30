# MicroPython script for ESP32
# Author: Himanshu Tripathi

# hardware interrupt example
# toggle the state of led with each button press
# also print the led state on terminal

from machine import Pin

# object for led
led = Pin(2,Pin.OUT)
# object for button
button = Pin(0,Pin.IN)

# interrupt service routine for button interrupt
def button_isr(pin):
    led.value(not led.value())
    print('LED is on' if led.value() else 'LED is off')
    

# enable interrupt request for button pin 
button.irq(trigger=Pin.IRQ_FALLING,handler=button_isr)

while True:
    pass 