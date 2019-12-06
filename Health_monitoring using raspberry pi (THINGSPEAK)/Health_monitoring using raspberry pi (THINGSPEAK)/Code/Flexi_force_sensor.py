
#*****************************************************************************************#
"""
Project Name : flexi force sensor with IOT"
IoT cloud : thingspeak
    E-mail : 
    Password : 

By:
    Madhusudhana AS
    Embedded Engg
    7760657379
    madhushivanand3@gmail.com
    Bangalore
"""

#*************************************************************************************#
import httplib
import urllib
import RPi.GPIO as GPIO
import time
import os

#***************************************************************************************#

DEBUG = 1
RCpin = 10

#**************************************************************************************#

GPIO.setmode(GPIO.BCM)

#**************************************************************************************#

def RCtime(RCpin):
    reading = 0
    GPIO.setup(RCpin, GPIO.OUT)

    GPIO.output(RCpin, GPIO.LOW)
    time.sleep(0.1)
 
    GPIO.setup(RCpin, GPIO.IN)
    # This takes about 1 millisecond per loop cycle
    while (GPIO.input(RCpin) == GPIO.LOW):
        reading += 1
    return reading

#**************************************************************************************#

while True:
    force = RCtime(RCpin)                                                  # Read RC timing using pin #18
    print "Applied Force : {0}". format(force)

    params = urllib.urlencode({'field4':  force,'key':'212Q9JLBZN7W1YEG'})  
    headers = {"Content-type": "application/x-www-form-urlencoded","Accept":"text/plain"}  
    conn = httplib.HTTPConnection("api.thingspeak.com:80")  
    conn.request("POST", "/update", params, headers)  
    response = conn.getresponse()  
    print response.status, response.reason  
    data = response.read()  
    conn.close()
    
    time.sleep(1)


#**************************************************************************************#

    
