# MicroPython Script for ESP32
# Author: Himanshu Tripathi

# ESP32 as web server (AP Mode)
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

# ***************************************
# web page
# ***************************************
def web_page():
    if isLedBlinking==True:
        led_state = 'Blinking'
        print('led is Blinking')
    else:
        if led.value()==1:
            led_state = 'ON'
            print('led is ON')
        elif led.value()==0:
            led_state = 'OFF'
            print('led is OFF')

    html_page = """    
    <html>    
    <head>    
     <meta content="width=device-width, initial-scale=1" name="viewport"></meta>    
    </head>    
    <body>    
     <center><h2>ESP32 Web Server in MicroPython </h2></center>    
     <center>    
      <form>    
      <button name="LED" type="submit" value="1"> LED ON </button>    
      <button name="LED" type="submit" value="0"> LED OFF </button>  
      <button name="LED" type="submit" value="2"> LED BLINK </button>   
      </form>    
     </center>    
     <center><p>LED is now <strong>""" + led_state + """</strong>.</p></center>    
    </body>    
    </html>"""  
    return html_page   

timer0 = machine.Timer(0)
def handle_callback(timer):
    led.value(not led.value())
isLedBlinking = False

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
    led_on = request.find('/?LED=1')
    led_off = request.find('/?LED=0')
    led_blink = request.find('/?LED=2')
    if led_on == 6:
        # turn on the LED
        print('LED ON')
        led.value(1)
        if isLedBlinking == True:
            timer0.deinit()
            isLedBlinking = False
    elif led_off == 6:
        # turn off the LED
        print('LED OFF')
        led.value(0)
        if isLedBlinking == True:
            timer0.deinit()
            isLedBlinking = False
    elif led_blink == 6:
        # blink the LED
        print('LED is Blinking')
        isLedBlinking = True
        timer0.init(period=500,mode=machine.Timer.PERIODIC,callback=handle_callback)
    # send response back to client machine 
    response = web_page()
    conn.send('HTTP/1.1 200 OK\n')
    conn.send('Content-Type: text/html\n')
    conn.send('Connection: close\n\n')
    conn.sendall(response)
    # close the connection
    conn.close()
