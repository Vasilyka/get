import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
leds = [16, 12, 25, 17, 27, 23, 22, 24]
GPIO.setup(leds, GPIO.OUT)
GPIO.output(leds, 0)
GPIO.setup(9, GPIO.IN)
GPIO.setup(10, GPIO.IN)
num = 0
def dec2bin(val):
    return [int(el) for el in bin(val)[2:].zfill(8)]
sleep_time = 0.2
while True:
    up = GPIO.input(9)
    down = GPIO.input(10)
    if up and down:
        GPIO.output(leds, 255)
    if up:
        if num != 255:
            num = num + 1
            print(num, dec2bin(num))
            time.sleep(sleep_time)
    if down:
        if num != 0:
            num = num - 1
            print(num, dec2bin(num))
            time.sleep(sleep_time)
    GPIO.output(leds, dec2bin(num))