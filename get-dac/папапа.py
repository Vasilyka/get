import r2r_dac as r2r
import signal_generator as sg
import time
import RPi.GPIO as GPIO
import smbus

amp = 3.2
sif = 10
saf = 1000
leds = [16,20,21,25,26,17,27,22]
dynamic_range=3.14
start = float(time.time())

class Triag:
    def __init__(self, led=12, F=200, v=1, f=0.05):
        GPIO.setmode(GPIO.BCM)
        self.led=led
        self.step=v
        self.tim=1/f
        self.f=F
        GPIO.setup(led, GPIO.OUT)
        pwm=GPIO.PWM(self.led, self.f)
        duty=0.0
        pwm.start(duty)
        while True:
            pwm.ChangeDutyCycle(duty)
            time.sleep(self.step)
            duty+=self.step
            if duty>=100.0 or duty<=0.0:
                self.step=-self.step


if __name__ == '__main__':
    try:
        dac = Triag(F=500, f=50)
    finally:
        dac.deinit()