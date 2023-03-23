##Refer to this Link https://medium.com/@anandmohan_8991/jetbot-using-l298n-pwm-motor-a6556ed358d6
import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

right_motor_pwm = 32
left_motor_pwm = 33

# for 1st Motor on ENA
M1B = 38
M1A = 37

M2B = 35
M2A = 36

# initialize EnA, In1 and In2
GPIO.setup(right_motor_pwm, GPIO.OUT)
GPIO.setup(left_motor_pwm, GPIO.OUT)

GPIO.setup(M1B, GPIO.OUT)
GPIO.setup(M1A, GPIO.OUT)
GPIO.setup(M2B, GPIO.OUT)
GPIO.setup(M2A, GPIO.OUT)

pwm = [GPIO.PWM(right_motor_pwm,50), GPIO.PWM(left_motor_pwm,50)]
pwm[0].start(0)
pwm[1].start(0)

try:
    while True:
        for dc in range(0, 50, 5): #start stop step
            print("Forward")
            GPIO.output(M1B, GPIO.HIGH)
            GPIO.output(M1A, GPIO.LOW)
            GPIO.output(M2B, GPIO.HIGH)
            GPIO.output(M2A, GPIO.LOW)
            pwm[0].ChangeDutyCycle(dc)
            pwm[1].ChangeDutyCycle(dc)
            time.sleep(0.1)

        for dc in range(0, 50, 5): #start stop step
            print("Backward")
            GPIO.output(M1B, GPIO.LOW)
            GPIO.output(M1A, GPIO.HIGH)
            GPIO.output(M2B, GPIO.LOW)
            GPIO.output(M2A, GPIO.HIGH)
            pwm[0].ChangeDutyCycle(dc)
            pwm[1].ChangeDutyCycle(dc)
            time.sleep(0.1)
except KeyboardInterrupt:
    pass
pwm[0].stop()
pwm[1].stop()
GPIO.cleanup()
