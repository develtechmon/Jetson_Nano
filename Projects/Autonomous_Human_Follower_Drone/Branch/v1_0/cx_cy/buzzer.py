import RPi.GPIO as GPIO
from time import sleep

buzzer_pin = 19

GPIO.setmode(GPIO.BOARD)
GPIO.setup(buzzer_pin, GPIO.OUT, initial=GPIO.LOW)

def alarm():
    GPIO.output(buzzer_pin,GPIO.HIGH)
    sleep(2)
    GPIO.output(buzzer_pin,GPIO.LOW)
    sleep(1)

