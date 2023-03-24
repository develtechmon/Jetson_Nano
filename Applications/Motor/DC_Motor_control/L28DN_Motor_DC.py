##Refer to this Link https://medium.com/@anandmohan_8991/jetbot-using-l298n-pwm-motor-a6556ed358d6
import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

left_motor_pwm = 33
right_motor_pwm = 32

left_motor = [35,36]
right_motor = [38,37]

GPIO.setup(left_motor_pwm, GPIO.OUT)
GPIO.setup(right_motor_pwm, GPIO.OUT)

GPIO.setup(left_motor[0], GPIO.OUT)
GPIO.setup(right_motor[0], GPIO.OUT)
GPIO.setup(left_motor[1], GPIO.OUT)
GPIO.setup(right_motor[1], GPIO.OUT)

pwm = [GPIO.PWM(32,50), GPIO.PWM(33,50)]

pwm[0].start(0)
pwm[1].start(0)

# Forwards
def forwards(dc):
    print("Forwards")
    GPIO.output(left_motor[0], GPIO.HIGH)
    GPIO.output(right_motor[0], GPIO.HIGH)
    GPIO.output(left_motor[1], GPIO.LOW)
    GPIO.output(right_motor[1], GPIO.LOW)

    pwm[0].ChangeDutyCycle(dc)
    pwm[1].ChangeDutyCycle(dc)
    time.sleep(0.1)

# Backwards
def backwards(dc):
    print("Backwards")
    GPIO.output(left_motor[0], GPIO.LOW)
    GPIO.output(right_motor[0], GPIO.LOW)
    GPIO.output(left_motor[1], GPIO.HIGH)
    GPIO.output(right_motor[1], GPIO.HIGH)

    pwm[0].ChangeDutyCycle(dc)
    pwm[1].ChangeDutyCycle(dc)
    time.sleep(0.1)


def stop():
    print("Forwards")
    GPIO.output(left_motor[0], GPIO.LOW)
    GPIO.output(right_motor[0], GPIO.LOW)
    pwm[0].ChangeDutyCycle(0)
    pwm[1].ChangeDutyCycle(0)

try:
    while True:
        for dc in range(0, 101, 5): #start stop step
            forwards(dc)
   
        for dc in range(0, 101, 5):
            backwards(dc)

except KeyboardInterrupt:
    stop()
    pass
pwm[0].stop()
pwm[1].stop()
GPIO.cleanup()
