import time
import RPi.GPIO as GPIO
#import Jetson.GPIO as GPIO  


# set pin numbers to the board's
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

right_motor = [32,33]

GPIO.setup(right_motor[0], GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(right_motor[1], GPIO.OUT, initial=GPIO.LOW)


pwm=[GPIO.PWM(32,50),GPIO.PWM(33,50)]
pwm[0].start(0)
pwm[1].start(0)


def forwards():
    for dc in range(0, 101, 5): #start stop step
        pwm[0].ChangeDutyCycle(dc)
        time.sleep(0.1)

def backwards():
    for dc in range(0, 101, 5): #start stop step
        pwm[1].ChangeDutyCycle(dc)
        time.sleep(0.1)

def stop():
    pwm[0].ChangeDutyCycle(0)
    pwm[1].ChangeDutyCycle(0)

try:
    while True:
        forwards()
        time.sleep(2)
        backwards()
except KeyboardInterrupt:
    stop()
    pass

stop()
pwm.stop()
GPIO.cleanup()


    

        