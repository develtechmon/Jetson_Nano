#https://sourceforge.net/p/raspberry-gpio-python/wiki/PWM/

import time
import RPi.GPIO as GPIO

pin = 35
GPIO.setmode(GPIO.BOARD)
GPIO.setup(pin, GPIO.OUT)

p = GPIO.PWM(pin, 50)  # channel=12 frequency=50Hz
p.start(0) # where dc is the duty cycle (0.0 <= dc <= 100.0)
try:
    while 1:
        for dc in range(0, 101, 5): #start stop step
            p.ChangeDutyCycle(dc)
            time.sleep(0.1)
        for dc in range(100, -1, -5):
            p.ChangeDutyCycle(dc)
            time.sleep(0.1)
except KeyboardInterrupt:
    pass
p.stop()
GPIO.cleanup()