import RPi.GPIO as GPIO  
import time

defaultSpeed = 50

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

rightFwd = 32
rightRev = 33
leftFwd = 35
leftRev = 12

#GPIO initialization
GPIO.setup(leftFwd, GPIO.OUT)
GPIO.setup(leftRev, GPIO.OUT)
GPIO.setup(rightFwd, GPIO.OUT)
GPIO.setup(rightRev, GPIO.OUT)

#Disable movement at startup
GPIO.output(leftFwd, False)
GPIO.output(leftRev, False)
GPIO.output(rightFwd, False)
GPIO.output(rightRev, False)

#PWM Initialization
rightMotorFwd = GPIO.PWM(rightFwd, 50)
leftMotorFwd = GPIO.PWM(leftFwd, 50)
rightMotorRev = GPIO.PWM(rightRev, 50)
leftMotorRev = GPIO.PWM(leftRev, 50)
rightMotorFwd.start(defaultSpeed)
leftMotorFwd.start(defaultSpeed)
leftMotorRev.start(defaultSpeed)
rightMotorRev.start(defaultSpeed)

def updatePwm(rightPwm, leftPwm):
	rightMotorFwd.ChangeDutyCycle(rightPwm)
	leftMotorFwd.ChangeDutyCycle(leftPwm)

def pwmStop():
	rightMotorFwd.ChangeDutyCycle(0)
	rightMotorRev.ChangeDutyCycle(0)
	leftMotorFwd.ChangeDutyCycle(0)
	leftMotorRev.ChangeDutyCycle(0)

if __name__ == '__main__':
    updatePwm(defaultSpeed,defaultSpeed)
	time.sleep(3)