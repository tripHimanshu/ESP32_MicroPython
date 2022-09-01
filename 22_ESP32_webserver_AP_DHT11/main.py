# MicroPython Script for ESP32
# Author: Himanshu Tripathi

# ESP32 as web server (AP Mode)
# This will display the values of
# temperature & humidity on web page
# using DHT11 Sensor

import machine
import network
import time
import sys
import gc
import dht
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

# Configure the ESP32 in access point mode
SSID = 'myESP'
PASSWORD = '123456789'
ap = network.WLAN(network.AP_IF)
ap.active(True)
ap.config(essid=SSID,password=PASSWORD)
timeout = 0
if not ap.active():
    print('Configuring...')
    while not ap.active() and timeout < 10:
        print(10-timeout)
        timeout += 1
        time.sleep(1)
    if ap.active():
        pass
    else:
        print('Could not configure')
        sys.exit()
print('network config: ',ap.ifconfig())

# DHT 11 sensor
d = dht.DHT11(machine.Pin(15))
# # DHT 22 Sensor
# d = dht.DHT22(machine.Pin(15))

# ***************************************
# web page
# ***************************************
def web_page():
    # Get the DHT readings
    d.measure()
    t = d.temperature()
    h = d.humidity()
    
    html_page = """<!DOCTYPE HTML>
    <html>  
        <head>  
            <meta name="viewport" content="width=device-width, initial-scale=1">  
            <meta http-equiv="refresh" content="1">  
        </head>  
        <body>  
            <center><h2>ESP32 Web Server in MicroPython </h2></center>  
            <center><p>Temperature is <strong>""" + str(t) + """ degree C.</strong>.</p></center>  
            <center><p>Humidity is <strong>""" + str(h) + """ %.</strong>.</p></center>  
        </body>  
    </html>"""  
    return html_page   



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
    try:
        time.sleep(2)
        # accept client connection 
        conn,addr = s.accept()
        print('client connected from ',addr)
        # recieve data from client machine
        request = conn.recv(1024)
        request = str(request)
        print('request content = ',request)
        try:
            # send response back to client machine 
            response = web_page()
            conn.send('HTTP/1.1 200 OK\n')
            conn.send('Content-Type: text/html\n')
            conn.send('Connection: close\n\n')
            conn.sendall(response)
            # close the connection
            conn.close()
        except Exception as e:
            print('Error>> ',str(e))
        
    except Exception as e:
        print('Error>> ',str(e))
        sys.exit()
    
