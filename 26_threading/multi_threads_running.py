# MicroPython Script for ESP32
# Author: Himanshu Tripathi

# tesing _thread module of MicroPython with ESP32
# running 3 threads in esp32
# 2 threads are created by _thread module
# one while loop is running as a separate thread

import _thread
import time 

# function for thread 1
def thread_1():
    n=0
    while True:
        print("I am thread 1- ",n)
        n += 1
        time.sleep(1)

# function for thread 2
def thread_2():
    n = 0
    while True:
        print("I am thread 2 - ",n)
        n += 1
        time.sleep(2)

# start the treads
# here we need to mention the function to be run by thread and arguments
# that we are passing to thread (function)
_thread.start_new_thread(thread_1,())
_thread.start_new_thread(thread_2,())

# forever loop (running as thread)
while True:
    print("I am thread 3")
    time.sleep(3)