# MicroPython Script for ESP32
# Author: Himanshu Tripathi

# bi-directional data communnication using thingspeak API
# temperature and humidity is read by the DHT 11 sensor
# This data is sent to thingspeak server using
# urequests POST method
# same data is received from thingspeak server using
# urequests GET method

import machine
import dht
import network
import urequests
import ujson as json
import time
import sys

# led object
led = machine.Pin(2,machine.Pin.OUT)
# DHT sensor object
d = dht.DHT11(machine.Pin(15))

# constants and variable
HTTP_HEADER = {'Content-Type':'application/json'}
THINGSPEAK_WRITE_API_KEY = 'F1WRX4CMXBCHUPSM'
UPDATE_INTERVAL = 5000 # time in ms
last_update = time.ticks_ms() # non-blocking delay

# ESP32 as station -- configuration
# connect with existing wifi network
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
timeout = 0
if not wlan.isconnected():
    wlan.connect('Arnav','chikuBhaiya24G')
    print('Connecting...')
    while not wlan.isconnected() and timeout < 10:
        print(10-timeout)
        timeout += 1
        time.sleep(1)
if wlan.isconnected():
    print('network config: ',wlan.ifconfig())
else:
    print('could not connect')
    sys.exit()

while True:
    if time.ticks_ms() - last_update > UPDATE_INTERVAL:
        d.measure()
        t = d.temperature()
        h = d.humidity()
        # put data into json format
        dht_readings = {'field1':t,'field2':h}
        # use post method from urequests method to write data on thingspeak
        request = urequests.post(
            'https://api.thingspeak.com/update?api_key='
            + THINGSPEAK_WRITE_API_KEY,
            json=dht_readings,headers=HTTP_HEADER)
        # close the request
        request.close()
        print(dht_readings)
        # Read data from thingspeak server
        # HTTP GET
        response = urequests.get('https://api.thingspeak.com/channels/1848070/fields/1.json?api_key=3W9NJYLYQ4YE44P2&results=2')
        # check status code of the request
        if response.status_code == 200:
            # get the data in json format
            data = response.json()
            print('received data')
            print(data)
        last_update = time.ticks_ms()