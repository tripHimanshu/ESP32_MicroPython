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

# DHT 11 sensor
d = dht.DHT11(machine.Pin(15))
# # DHT 22 Sensor
# d = dht.DHT22(machine.Pin(15))

# ***************************************
# web page (using AJAX)
# ***************************************
def web_page():
    html_page = """<!DOCTYPE html>  
    <html>  
    <head>  
        <meta name='viewport' content='width=device-width, initial-scale=1.0'/>  
        <script>   
            var ajaxRequest = new XMLHttpRequest();  
            function ajaxLoad(ajaxURL)  
            {  
                ajaxRequest.open('GET',ajaxURL,true);  
                ajaxRequest.onreadystatechange = function()  
                {  
                    if(ajaxRequest.readyState == 4 && ajaxRequest.status==200)
                    {
                        var ajaxResult = ajaxRequest.responseText;  
                        var tmpArray = ajaxResult.split("|");  
                        document.getElementById('temp').innerHTML = tmpArray[0];  
                        document.getElementById('humi').innerHTML = tmpArray[1];  
                    }  
                }  
                ajaxRequest.send();  
            }  
            function updateDHT()   
            {   
                ajaxLoad('getDHT');   
            }
            setInterval(updateDHT, 3000);  
        </script>  
        <title>ESP32 Weather Station</title>  
    </head>  
    <body>  
        <center>  
            <div id='main'>  
            <h1>MicroPython Weather Station</h1>  
            <h4>Web server on ESP32 | DHT values auto updates using AJAX.</h4>  
            <div id='content'>   
                <p>Temperature: <strong><span id='temp'>--.-</span> &deg;C</strong></p>  
                <p>Humidity: <strong><span id='humi'>--.-</span> % </strong></p>  
                </div>  
            </div>  
        </center>  
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
        # accept client connection 
        conn,addr = s.accept()
        print('client connected from ',addr)
        # recieve data from client machine
        request = conn.recv(1024)
        request = str(request)
        print('request content = ',request)
        try:
            # send updates
            update = request.find('/getDHT')
            if update == 6:
                d.measure()
                t = d.temperature()
                h = d.humidity()
                response = str(t) + "|" + str(h)
            else:
                response = web_page()
            # create a socket reply
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
    
