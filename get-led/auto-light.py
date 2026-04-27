import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
led = 26
button = 13
photor = 6
GPIO.setup(photor, GPIO.IN)
GPIO.setup(led, GPIO.OUT)
state = 0
period = 0
while True:
    state = not(GPIO.input(photor))
    GPIO.output(led, state)
    #time.sleep(period)