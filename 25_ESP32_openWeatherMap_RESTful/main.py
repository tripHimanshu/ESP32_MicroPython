# MicroPython Script for ESP32
# Author: Himanshu Tripathi

# Reading values from open weather web 
# using its RESTful API
# REST API is one of the most popular API types
# REST stands for REpresentational State Transfer
# it is also known as RESTful API
# before running the code please replace these values in the code
# your city
# your api key
# your ssid
# your psk

import machine
import network
import time
import sys
import gc
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

# constants and variables
BASE_URL = 'https://api.openweathermap.org/data/2.5/weather?q='
CITY = 'your city'
API_KYE = 'your api key'
URL = BASE_URL+CITY+'&appid='+API_KYE
UPDATE_INTERVAL = 5000 # ms
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

# Forever loop
while True:
    if time.ticks_ms() - last_update > UPDATE_INTERVAL:
        # send weather data request
        response = urequests.get(URL)
        # check the status code of request
        if response.status_code == 200:
            # get the data in json format
            data = response.json()
            # get the main dict block for weather data
            main = data['main']
            # get the temperature and subtract it with 273.15
            # to convert it in degree celcius (default value in Kelvin)
            temperature = main['temp'] - 273.15
            # get the humidity in %
            humidity = main['humidity']
            # get the pressure in hPA
            pressure = main['pressure']
            # get the weather report
            report = data['weather']
            # print the data on terminal
            print("City: {}".format(CITY))
            print("Temperature: {:.1f} {}C".format(temperature,chr(176)))
            print("Humidity: {} %".format(humidity))
            print("Pressure: {} hPA".format(pressure))
            print("Weather Report: {}".format(report[0]['description']))
        else:
            # show error message
            print("Error in HTTP Request")
        led.value(not led.value())
        last_update = time.ticks_ms()
            


