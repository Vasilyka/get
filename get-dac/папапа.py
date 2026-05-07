import RPi.GPIO as GPIO
import time

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

if __name__ == "__main__":
    try:
        dac = R2R_DAC(16, 500, 3.183, True)
        while True:
            try:
                voltage = float(input('Введите напряжение: '))
                dac.set_voltage(voltage)
            except ValueError:
                print('Вы ввели не число...зачем...')
            except KeyboardInterrupt:
                print('Thank you for using RaspberryPie, bye!')
    finally:
        dac.deinit()