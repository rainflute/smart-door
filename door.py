import RPi.GPIO as GPIO
from time import sleep


def lock():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(7, GPIO.OUT)
    # set pin 7 at 50hz
    try:
        p = GPIO.PWM(7, 50)
        p.start(7.5)
        p.ChangeDutyCycle(12.0)
        sleep(0.5)
        p.stop()
        print ('Door locked')
    except KeyboardInterrupt:
        GPIO.cleanup()


def open():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(7, GPIO.OUT)
    # set pin 7 at 50hz
    try:
        p = GPIO.PWM(7, 50)
        p.start(7.5)
        p.ChangeDutyCycle(2.7)
        sleep(0.5)
        p.stop()
        print('Door opened')
    except KeyboardInterrupt:
        GPIO.cleanup()
