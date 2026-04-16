import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)
led = 26
GPIO.setup(led, GPIO.OUT)
state = 0
period = 1.5
button = 13
GPIO.setup(button, GPIO.IN)
while True:
    state = not state
    GPIO.output(led, state)
    time.sleep(0.2)