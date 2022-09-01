# MicroPython Script for ESP32
# Author: Himanshu Tripathi

# ESP32 as web server
# with the web server with ON and OFF buttons
# control the on-board LED of ESP32

import machine
import network
import time
import sys
import gc
try:
    import usocket as socket
except:
    import socket

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
wlan.connect('your_ssid','your_password')
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
   
# ***************************************
# web page
# ***************************************
def web_page():
  if led.value() == 1:
    gpio_state="ON"
  else:
    gpio_state="OFF"
  
  html = """<html><head> <title>ESP Web Server</title> <meta name="viewport" content="width=device-width, initial-scale=1">
  <link rel="icon" href="data:,"> <style>html{font-family: Helvetica; display:inline-block; margin: 0px auto; text-align: center;}
  h1{color: #0F3376; padding: 2vh;}p{font-size: 1.5rem;}.button{display: inline-block; background-color: #e7bd3b; border: none; 
  border-radius: 4px; color: white; padding: 16px 40px; text-decoration: none; font-size: 30px; margin: 2px; cursor: pointer;}
  .button2{background-color: #4286f4;}</style></head><body> <h1>ESP Web Server</h1> 
  <p>GPIO state: <strong>""" + gpio_state + """</strong></p><p><a href="/?led=on"><button class="button">ON</button></a></p>
  <p><a href="/?led=off"><button class="button button2">OFF</button></a></p></body></html>"""
  return html

# create server socket at esp32
# if socket is not created, script terminated
try:
    # create socket (TCP)
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    # bind the socket with IP and PORT
    # blank IP specifies that socket is reachable by any addr
    # the machine happens to have
    # web server port is 80
    s.bind(('',80))
    # start listening for clients 
    s.listen(5)
    print('Socket created')
except Exception as e:
    print('Error>>',str(e))
    sys.exit()

# forever loop 
while True:
    # accept client connection 
    conn,addr = s.accept()
    print('client connected from ',addr)
    # recieve data from client machine
    request = conn.recv(1024)
    request = str(request)
    print('request content = ',request)
    # find the request 
    led_on = request.find('/?led=on')
    led_off = request.find('/?led=off')
    if led_on == 6:
        # turn on the LED
        print('LED ON')
        led.value(1)
    if led_off == 6:
        # turn off the LED
        print('LED OFF')
        led.value(0)
    # send response back to client machine 
    response = web_page()
    conn.send('HTTP/1.1 200 OK\n')
    conn.send('Content-Type: text/html\n')
    conn.send('Connection: close\n\n')
    conn.sendall(response)
    # close the connection
    conn.close()
