import RPi.GPIO as GPIO
import time

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(5, GPIO.OUT)

while(True):
    GPIO.output(5, 1)
    time.sleep(1)
    GPIO.output(5, 0)
    time.sleep(1)