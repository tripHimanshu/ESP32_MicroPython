# MicroPython Script for ESP32
# Author: Himanshu Tripathi

# connect ESP32 with wifi using timeout
# access wbsite data using requests method

import network
import time
import urequests

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
    return wlan

# connect esp32 with wifi network (with timeout)
wlan = wifi_connect('ssid','psk',5)
print('The IP of ESP32 is: ')
print(wlan.ifconfig())
# usign get method from urequests module to read data
if wlan.isconnected():
    req = urequests.get('https://example.com')
    # if status code received is 200, requested successfully
    print('request successfull' if req.status_code == 200 else 'failed')
    # print the result in text format
    print(req.text)
else:
    print('request to read failed')