# MicroPython Script for ESP32
# Author: Himanshu Tripathi

# ESP32 Weather Station with DHT11 Sensor
# on Thingspeak (RESTful API)
# REST API is one of the most popular API types
# REST stands for REpresentational State Transfer
# it is also known as RESTful API

import machine
import network
import time
import sys
import gc
import dht
import urequests

# run garbage collector
# it is a form of automatic memory management
# this is a way to reclaim memory occupied with objects
# that are no longer in use by the program
# this is usefull to save space in memory
gc.collect()

# object for on-board led 
led = machine.Pin(2,machine.Pin.OUT)
# default status of led is OFF
led.off()
# DHT 11 sensor object
d = dht.DHT11(machine.Pin(15))
# # DHT 22 Sensor
# d = dht.DHT22(machine.Pin(15))

# constants and variables
HTTP_HEADERS = {'Content-Type' : 'application/json'}
THINGSPEAK_WRITE_API_KEY = 'your API key'
UPDATE_TIME_INTERVAL = 5000 # ms
last_update = time.ticks_ms()

# connect ESP32 with existing WiFi network
# it will try to connect with network for only 10 seconds
# if not connected with network, script terminated
timeout = 0
# configure esp32 in station mode 
wlan = network.WLAN(network.STA_IF)
wlan.active(False)
time.sleep(0.5)
# enable wifi module (hardware)
wlan.active(True)
wlan.connect('your ssid','your psk')
if not wlan.isconnected():
    print('Connecting to network..')
    while not wlan.isconnected() and timeout < 10:
        print(10-timeout)
        timeout += 1
        time.sleep(1)
    if wlan.isconnected():
        # print the ip addr of esp32 in network
        print('network config: ',wlan.ifconfig())
    else:
        print('could not connect')
        sys.exit()

# Forever Loop
while True:
    # wait for the update sensor data using non-blocking delay
    if time.ticks_ms()-last_update > UPDATE_TIME_INTERVAL:
        # measure sensor data
        d.measure()
        t = d.temperature()
        h = d.humidity()
        # put data into json format
        dht_readings = {'field1':t, 'field2':h}
        # use post method from urequests module to write data on thingspeak
        request = urequests.post(
            'https://api.thingspeak.com/update?api_key=' + THINGSPEAK_WRITE_API_KEY,
            json=dht_readings,headers=HTTP_HEADERS)
        # close the request
        request.close()
        # print DHT sensor reading on terminal
        print(dht_readings)
        # toggle the LED status for visulization at hardware level
        led.value(not led.value())
        # update the last update time 
        last_update = time.ticks_ms()



