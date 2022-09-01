# MicroPython Script for ESP32
# Author: Himanshu Tripathi

# ESP32 Wi-Fi Station Mode

import network

# object for wlan
wlan = network.WLAN(network.STA_IF)
# activate wifi driver
wlan.active(True)

# scan the nearby network
networks = wlan.scan()
# print the available wifi networks
print(networks)
        
