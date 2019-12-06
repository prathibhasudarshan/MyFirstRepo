
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
SPOpin = 20

#**************************************************************************************#

GPIO.setwarnings(False)

GPIO.setmode(GPIO.BCM)

GPIO.setup(21 ,GPIO.OUT)


GPIO.output(21 , GPIO.HIGH)

#**************************************************************************************#

def RCtime(SPOpin):
    reading = 0
    GPIO.setup(SPOpin, GPIO.OUT)

    GPIO.output(SPOpin, GPIO.LOW)
    time.sleep(0.1)
 
    GPIO.setup(SPOpin, GPIO.IN)
    # This takes about 1 millisecond per loop cycle
    while (GPIO.input(SPOpin) == GPIO.LOW):
        reading += 1
    return reading

#**************************************************************************************#

while True:
    SPO = RCtime(SPOpin)                                                  # Read RC timing using pin #18
    print "Blood Oxygen : {0}". format(SPO)

    params = urllib.urlencode({'field3':  SPO,'key':'212Q9JLBZN7W1YEG'})  
    headers = {"Content-type": "application/x-www-form-urlencoded","Accept":"text/plain"}  
    conn = httplib.HTTPConnection("api.thingspeak.com:80")  
    conn.request("POST", "/update", params, headers)  
    response = conn.getresponse()  
    print response.status, response.reason  
    data = response.read()  
    conn.close()
    
    time.sleep(1)


#**************************************************************************************#

    
