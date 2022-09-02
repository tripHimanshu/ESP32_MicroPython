# MicroPython Script for ESP32
# Author: Himanshu Tripathi

# connect ESP32 with wifi using timeout
# enter your ssid and password in place of 'ssid' & 'psk'
# in the function call statement 

import network
import time

# # global variable
# timeout = 0
# 
# # wifi object
# wlan = network.WLAN(network.STA_IF)
# # restart wifi module of esp32
# wlan.active(False)
# time.sleep(0.5)
# wlan.active(True)
# 
# # connect with existing wifi
# wlan.connect('ssid','psk')
# 
# if not wlan.isconnected():
#     print('Connecting...')
#     while not wlan.isconnected() and timeout< 10:
#         print(10-timeout)
#         timeout += 1
#         time.sleep(1)
# if wlan.isconnected():
#     print('Connection established')
# else:
#     print('Could not connect')

# function to connect with wifi
def wifi_connect(ssid,psk,timeout):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    t = 0
    if not wlan.isconnected():
        print('Connecting with network..')
        while (not wlan.isconnected() and t<timeout):
            print(timeout-t)
            t += 1
            time.sleep(1)
    if wlan.isconnected():
        print('connected successfully')
    else:
        print('Could not connect') 

wifi_connect('ssid','psk',5)