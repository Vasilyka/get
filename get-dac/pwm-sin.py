import signal_generator as sg
import time
import RPi.GPIO as GPIO


amp = 3.2
sif = 10
saf = 1000
start = float(time.time())

GPIO.setmode(GPIO.BCM)
leds = [16,12,25,17,27,23,22,24]
GPIO.setup(leds, GPIO.OUT)
GPIO.output(leds, 0)
dynamic_range=3.3

class R2R_DAC:
    def __init__(self, gpio_pin, pwm_freq, dynamic_range, verbose=False):
        self.gpio_pin = gpio_pin
        self.pwm_freq = pwm_freq
        self.dynamic_range = dynamic_range
        self.verbose = verbose

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.gpio_pin, GPIO.OUT, initial = 0)


        self.pwm = GPIO.PWM(self.gpio_pin, self.pwm_freq)
        self.pwm.start(100)


    def deinit(self):
        GPIO.output(self.gpio_pin, 0)
        GPIO.cleanup()

    def set_number(self, number):
        return[int(el) for el in bin(number)[2:].zfill(8)]

    def set_voltage(self, voltage):
        if not(0.0<=voltage<=dynamic_range):
            print('Напряжение за рамками диапазона, сброс до 0.0 В')
            duty = 0
        else:
            duty = voltage/self.dynamic_range
            print(duty)
        self.pwm.ChangeDutyCycle(duty*100)


if __name__ == '__main__':
    try:
        dac = R2R_DAC(12, 500, dynamic_range, True)
        while True:
            try:
                dac.set_voltage((sg.get_sin_wave_amplitude(sif, 2)/2)*amp)
                time.sleep(1/saf)
            except ValueError:
                print('aaaa')
    finally:
        dac.deinit()