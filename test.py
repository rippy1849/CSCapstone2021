import RPi.GPIO as GPIO
import time

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(3, GPIO.OUT)
pwm=GPIO.PWM(3,50)
pwm.start(0)

def SetAngle(angle):
    duty = angle/18 +2
    GPIO.output(3, 1)
    pwm.ChangeDutyCycle(duty)
    time.sleep(1)
    GPIO.output(3, 0)
    pwm.ChangeDutyCycle(0)


for i in range(1,19):
    SetAngle(i*10)
    print("Turn", i)


