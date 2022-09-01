# MicroPython Script for ESP32
# Author: Himanshu Tripathi

# ESP32 Wi-Fi Access Point Mode

import network

# object for wlan
wlan = network.WLAN(network.AP_IF)
# activate wifi driver
wlan.active(True)

# wifi configuration for esp32
wlan.config(essid='myESP32',password='123456789',authmode=network.AUTH_WPA_WPA2_PSK)
print(wlan.ifconfig())
        
