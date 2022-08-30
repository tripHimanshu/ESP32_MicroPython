# MicroPython script for ESP32
# Author: Himanshu Tripathi

# Servo motor class for multiple functionality
# servo motor used is Tower Pro Micro Servo 9g

import machine
import time

class Servo:
    """
    Servo motor class
    import module: machine
    """
    # initialization method
    def __init__(self,pin):
        self.pin = pin
        self.pwm = machine.PWM(machine.Pin(self.pin),freq=50)
    # map method  
    def map(self,x,in_min,in_max,out_min,out_max):
        return int((x-in_min) * (out_max-out_min) / (in_max-in_min) + out_min)
    # method to set angle of servo motor   
    def set_angle(self,angle):
        self.pwm.duty(self.map(angle,0,180,18,140))
    # method to rotate servo from one position to other position
    def change_position(self,start_pos,end_pos,step,delay):
        if step > 0:
            self.end_pos = end_pos + 1
        elif step < 0:
            self.end_pos = end_pos - 1
        for i in range (start_pos,end_pos,step):
            self.set_angle(i)
            time.sleep_ms(delay)
        
    
# object for servo motor 
my_servo = Servo(13)

while True:
    # set servo at 0 position
    my_servo.set_angle(0)
    # start rotating servo 
    my_servo.change_position(0,180,10,500)
    time.sleep(2)
    my_servo.change_position(180,0,-10,500)
    time.sleep(2)
        