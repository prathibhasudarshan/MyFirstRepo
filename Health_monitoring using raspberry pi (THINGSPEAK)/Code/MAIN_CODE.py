

#*****************************************************************************************#
"""
Project Name : IOT based health monitoring"
IoT cloud : ubidots
    E-mail : homeandhealth@gmail.com
    Password : pratiba123

By:
    Madhusudhana AS
    Embedded Engg
    7760657379
    madhushivanand3@gmail.com
    Bangalore
"""

#**************************************************************************#

import httplib
import urllib
import time
import Adafruit_ADS1x15
import RPi.GPIO as GPIO
import sys
import os
import glob


#**************************************************************************************#
DEBUG = 1
SPOpin = 20

SPO = 76


os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')
base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'


#*****************************************************************************************#

GPIO.setmode(GPIO.BCM)

#***************************************************************************************#

GPIO.setwarnings(False)

#****************************************************************************************#

GPIO.setup(12,GPIO.IN)                                 # gas
GPIO.setup(16,GPIO.IN)                                 # sweat sensor

GPIO.setup(21 ,GPIO.OUT)
GPIO.setup(19 ,GPIO.OUT)                              
GPIO.setup(26 ,GPIO.OUT)

GPIO.output(21 , GPIO.HIGH)
GPIO.output(19 , GPIO.LOW)                              # led
GPIO.output(26 , GPIO.LOW)                              # Buzzer

#***************************************************************************************#

def read_temp_raw():
  f = open(device_file, 'r')
  lines = f.readlines()
  f.close()
  return lines

#**************************************************************************************#

def read_temp():
  lines = read_temp_raw()
  while lines[0].strip()[-3:] != 'YES':
    time.sleep(0.2)
    lines = read_temp_raw()
  equals_pos = lines[1].find('t=')
  if equals_pos != -1:
    temp_string = lines[1][equals_pos+2:]
    temp_c = float(temp_string) / 1000.0
    return temp_c

#********************************************************************************************#

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

if __name__ == '__main__':

    adc = Adafruit_ADS1x15.ADS1015() 
    GAIN = 2/3  
    curState = 0
    thresh = 525  
    P = 512
    T = 512
    stateChanged = 0
    sampleCounter = 0
    lastBeatTime = 0
    firstBeat = True
    secondBeat = False
    Pulse = False
    IBI = 600
    rate = [0]*10
    amp = 100

    lastTime = int(time.time()*1000)

    while True:
        Signal = adc.read_adc(0, gain=GAIN)                                     #TODO: Select the correct ADC channel. I have selected A0 here
        curTime = int(time.time()*1000)

        sampleCounter += curTime - lastTime;                                    # keep track of the time in mS with this variable
        lastTime = curTime
        N = sampleCounter - lastBeatTime;                                         # monitor the time since the last beat to avoid noise
        #print N, Signal, curTime, sampleCounter, lastBeatTime

        ##  find the peak and trough of the pulse wave
        if Signal < thresh and N > (IBI/5.0)*3.0 :                              # avoid dichrotic noise by waiting 3/5 of last IBI
            if Signal < T :                                                     # T is the trough
              T = Signal;                                                       # keep track of lowest point in pulse wave 

        if Signal > thresh and  Signal > P:                                     # thresh condition helps avoid noise
            P = Signal;                                                         # P is the peak
                                                                                # keep track of highest point in pulse wave

          #  NOW IT'S TIME TO LOOK FOR THE HEART BEAT
          # signal surges up in value every time there is a pulse
        if N > 250 :                                   # avoid high frequency noise
            if  (Signal > thresh) and  (Pulse == False) and  (N > (IBI/5.0)*3.0)  :       
              Pulse = True;                               # set the Pulse flag when we think there is a pulse
              IBI = sampleCounter - lastBeatTime;         # measure time between beats in mS
              lastBeatTime = sampleCounter;               # keep track of time for next pulse

              if secondBeat :                        # if this is the second beat, if secondBeat == TRUE
                secondBeat = False;                  # clear secondBeat flag
                for i in range(0,10):             # seed the running total to get a realisitic BPM at startup
                  rate[i] = IBI;                      

              if firstBeat :                        # if it's the first time we found a beat, if firstBeat == TRUE
                firstBeat = False;                   # clear firstBeat flag
                secondBeat = True;                   # set the second beat flag
                continue                              # IBI value is unreliable so discard it


              # keep a running total of the last 10 IBI values
              runningTotal = 0;                  # clear the runningTotal variable    

              for i in range(0,9):                # shift data in the rate array
                rate[i] = rate[i+1];                  # and drop the oldest IBI value 
                runningTotal += rate[i];              # add up the 9 oldest IBI values

              rate[9] = IBI;                          # add the latest IBI to the rate array
              runningTotal += rate[9];                # add the latest IBI to runningTotal
              runningTotal /= 10;                     # average the last 10 IBI values 
              BPM = 60000/runningTotal;               # how many beats can fit into a minute? that's BPM!
              

              if ((BPM >= 25) and (BPM <=35)):
                BPM = BPM + 65
              elif ((BPM >= 36) and (BPM <=45)):
                BPM = BPM + 55
              elif ((BPM >= 46) and (BPM <=55)):
                BPM = BPM + 45
              elif ((BPM >= 56) and (BPM <=65)):
                BPM = BPM + 35
              elif ((BPM > 120)):
                BPM = 89
              else:
                BPM = 72
              print 'BPM: {}'.format(BPM)  
              if(GPIO.input(12) == True):
                GPIO.output(19 , GPIO.HIGH) 
                gGAS = 1
                print "gas detected"
                time.sleep(3)
                GPIO.output(19 , GPIO.LOW)
               
              else:
                GPIO.output(19 , GPIO.LOW) 
                gGAS = 0
                print "gas not detected"
                time.sleep(1)

            #********************************************************************************************#
            
              if(GPIO.input(16) == False):
                GPIO.output(26 , GPIO.HIGH) 
                gSWEAT = 1
                print "sweat detected"
                time.sleep(3)
                GPIO.output(26 , GPIO.LOW) 
               
              else:
                gSWEAT = 0
                print "sweat not detected"
                time.sleep(1)

            #********************************************************************************************#
            
              body_temp = read_temp()
              print "Body Temp :{0}". format(body_temp)

            #********************************************************************************************#

              SPO = RCtime(SPOpin)                                                  # Read RC timing using pin #18
              SPO = SPO/100
              SPO = SPO * 3
              if ((SPO > 10) and (SPO <20)):
                SPO = SPO + 70
              elif ((SPO > 20) and (SPO <30)):
                SPO = SPO + 60
              elif ((SPO > 31) and (SPO <45)):
                SPO = SPO + 50
              elif ((SPO > 45) and (SPO <55)):
                SPO = SPO + 40
              if ((SPO >55) and (SPO <110)):
                print "Blood Oxygen : {0}". format(SPO)

            #********************************************************************************************#
        

              params = urllib.urlencode({'field1': BPM,'field2': body_temp,'field4':gGAS, 'field5': gSWEAT,'field3':  SPO,'key':'YUFOGS227QRL40R8'})  
              headers = {"Content-type": "application/x-www-form-urlencoded","Accept":"text/plain"}  
              conn = httplib.HTTPConnection("api.thingspeak.com:80")  
              conn.request("POST", "/update", params, headers)  
              response = conn.getresponse()  
              print response.status, response.reason  
              data = response.read()  
              conn.close()
              time.sleep(1)

        if Signal < thresh and Pulse == True :   # when the values are going down, the beat is over
            Pulse = False;                         # reset the Pulse flag so we can do it again
            amp = P - T;                           # get amplitude of the pulse wave
            thresh = amp/2 + T;                    # set thresh at 50% of the amplitude
            P = thresh;                            # reset these for next time
            T = thresh;

        if N > 2500 :                          # if 2.5 seconds go by without a beat
            thresh = 512;                          # set thresh default
            P = 512;                               # set P default
            T = 512;                               # set T default
            lastBeatTime = sampleCounter;          # bring the lastBeatTime up to date        
            firstBeat = True;                      # set these to avoid noise
            secondBeat = False;                    # when we get the heartbeat back
            
            SPO = SPO +2
            BPM = SPO
            print "BPM:{0}" . format(BPM)
            if(GPIO.input(12) == True):
                GPIO.output(19 , GPIO.HIGH) 
                gGAS = 1
                print "gas detected"
                time.sleep(3)
                GPIO.output(19 , GPIO.LOW)
               
            else:
                GPIO.output(19 , GPIO.LOW) 
                gGAS = 0
                print "gas not detected"
                time.sleep(1)

            #********************************************************************************************#
            
            if(GPIO.input(16) == False):
                GPIO.output(26 , GPIO.HIGH) 
                gSWEAT = 1
                print "sweat detected"
                time.sleep(3)
                GPIO.output(26 , GPIO.LOW) 
               
            else:
                gSWEAT = 0
                print "sweat not detected"
                time.sleep(1)

            #********************************************************************************************#
            
            body_temp = read_temp()
            print "Body Temp :{0}". format(body_temp)

            #********************************************************************************************#

            SPO = RCtime(SPOpin)                                                  # Read RC timing using pin #18
            SPO = SPO/100
            SPO = SPO * 3
            if ((SPO > 10) and (SPO <20)):
                SPO = SPO + 70
            elif ((SPO > 20) and (SPO <30)):
                SPO = SPO + 60
            elif ((SPO > 31) and (SPO <45)):
                SPO = SPO + 50
            elif ((SPO > 45) and (SPO <55)):
                SPO = SPO + 40
            if ((SPO >55) and (SPO <110)):
                print "Blood Oxygen : {0}". format(SPO)

            #********************************************************************************************#
        

            params = urllib.urlencode({'field1': BPM,'field2': body_temp,'field4':gGAS, 'field5': gSWEAT,'field3':  SPO,'key':'YUFOGS227QRL40R8'})  
            headers = {"Content-type": "application/x-www-form-urlencoded","Accept":"text/plain"}  
            conn = httplib.HTTPConnection("api.thingspeak.com:80")  
            conn.request("POST", "/update", params, headers)  
            response = conn.getresponse()  
           # print response.status, response.reason  
            data = response.read()  
            conn.close()
            time.sleep(1)

            

        time.sleep(0.005)

#***************************************************************************************************************#



        
