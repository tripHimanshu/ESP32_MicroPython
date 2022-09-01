# MicroPython Script for ESP32
# Author: Himanshu Tripathi

# Connect ESP32 with wifi network
# Note: before running the code
# enter your network ssid in place of 'ssid_name'
# enter your network password in place of 'password'

import network

# object for wlan
wlan = network.WLAN(network.STA_IF)
# activate wifi driver
wlan.active(True)

# connect esp32 with some existing wifi network
wlan.connect('ssid_name','password')
# show the connection status
if wlan.isconnected():
    print('Connection established')
