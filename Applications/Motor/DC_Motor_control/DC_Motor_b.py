#!/usr/bin/env python

#import Jetson.GPIO as GPIO  
import RPi.GPIO as GPIO
import time

#Supported PWM Pin 12,32,33,35
#https://forums.developer.nvidia.com/t/how-do-i-use-pwm-on-jetson-nano/72595/9

# for 1st Motor on ENA
M2B = 32
M2A = 33

M1B = 35
M1A = 12

# set pin numbers to the board's
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

# initialize EnA, In1 and In2
GPIO.setup(M2B, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(M2A, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(M1B, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(M1A, GPIO.OUT, initial=GPIO.LOW)

# Stop
GPIO.output(M2B, GPIO.LOW)
GPIO.output(M2A, GPIO.LOW)
GPIO.output(M1B, GPIO.LOW)
GPIO.output(M1A, GPIO.LOW)
time.sleep(1)

# Forward
GPIO.output(M2B, GPIO.HIGH)
GPIO.output(M2A, GPIO.LOW)
GPIO.output(M1B, GPIO.HIGH)
GPIO.output(M1A, GPIO.LOW)

time.sleep(1)

# Stop
GPIO.output(M2B, GPIO.LOW)
GPIO.output(M2A, GPIO.LOW)
GPIO.output(M1B, GPIO.LOW)
GPIO.output(M1A, GPIO.LOW)
time.sleep(1)

# Backward
GPIO.output(M2B, GPIO.LOW)
GPIO.output(M2A, GPIO.HIGH)
GPIO.output(M1B, GPIO.LOW)
GPIO.output(M1A, GPIO.HIGH)
time.sleep(1)

# Stop
GPIO.output(M2B, GPIO.LOW)
GPIO.output(M2A, GPIO.LOW)
GPIO.output(M1B, GPIO.LOW)
GPIO.output(M1A, GPIO.LOW)
time.sleep(1)

GPIO.cleanup()
