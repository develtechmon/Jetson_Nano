#!/usr/bin/env python

import Jetson.GPIO as GPIO  
#import RPi.GPIO as GPIO
import time

# for 1st Motor on ENA
M2B = 35#32
M2A = 36#33

M1B = 38#12
M1A = 37#35
# set pin numbers to the board's
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

# initialize EnA, In1 and In2
GPIO.setup(M2B, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(M2A, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(M1B, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(M1A, GPIO.OUT, initial=GPIO.LOW)

def Forwards():
    # Forward
    GPIO.output(M2B, GPIO.HIGH)
    GPIO.output(M2A, GPIO.LOW)
    GPIO.output(M1B, GPIO.HIGH)
    GPIO.output(M1A, GPIO.LOW)
    
def Backwards():
    # Backward
    GPIO.output(M2B, GPIO.LOW)
    GPIO.output(M2A, GPIO.HIGH)
    GPIO.output(M1B, GPIO.LOW)
    GPIO.output(M1A, GPIO.HIGH)

try:
    while True:
        Forwards()
        time.sleep(1)
        #Backwards()
except KeyboardInterrupt:
    GPIO.cleanup()