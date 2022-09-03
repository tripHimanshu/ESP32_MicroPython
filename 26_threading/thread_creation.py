# MicroPython Script for ESP32
# Author: Himanshu Tripathi

# tesing _thread module of MicroPython with ESP32

import _thread

def thread_1():
    print("I am thread 1")
    
_thread.start_new_thread(thread_1,())

print("I am thread 2")