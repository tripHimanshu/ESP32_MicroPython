# MicroPython Script for ESP32
# Author: Himanshu Tripathi

# testing the maximum number of threads
# that we may run on ESP32
# I found that 15 threads can be run on ESP32 DEVKIT V1

import _thread
import time

# use mutex 
mutex = _thread.allocate_lock()
# global variable
number = 0

# function to be called for thread
def hello(number):
    while True:
        mutex.acquire() # acquire lock 
        print('Hello Word - ',number)
        time.sleep(1)
        mutex.release() # lock release
        #_thread.exit()

try:
    for i in range(0,20):
        number += 1
        _thread.start_new_thread(hello,(number,))
except:
    print('Error')

