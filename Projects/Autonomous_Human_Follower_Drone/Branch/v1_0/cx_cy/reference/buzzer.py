import RPi.GPIO as GPIO
import time


buzzer_pin = 19

def main():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(buzzer_pin, GPIO.OUT, initial=GPIO.LOW)

    while True:
        GPIO.output(buzzer_pin,GPIO.HIGH)
        print("Beep")
        time.sleep(1)
        GPIO.output(buzzer_pin,GPIO.LOW)
        print("Off")
        time.sleep(1)

if __name__ == '__main__':
    main()

