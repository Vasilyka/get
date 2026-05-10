import time
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
dynamic_range = 3.162
class PWM_DAC:
    def __init__(self, gpio_pin, pwm_freq, dynamic_range, verbose=False):
        self.gpio_pin = gpio_pin
        self.pwm_freq = pwm_freq
        self.dynamic_range = dynamic_range
        self.verbose = verbose

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.gpio_pin, GPIO.OUT, initial = 0)


        self.pwm = GPIO.PWM(self.gpio_pin, self.pwm_freq)
        self.pwm.start(0)


    def deinit(self):
        self.pwm.stop()
        GPIO.output(self.gpio_pin, 0)
        GPIO.cleanup()

    def set_voltage(self, voltage):
        if not(0.0<=voltage<=self.dynamic_range):
            print(f"Напряжение выходит за динамический диапазон ЦАП (0.00 - {dynamic_range:.2f} В)")
            duty = 0
        else:
            duty = voltage/self.dynamic_range
            print(duty)
        self.pwm.ChangeDutyCycle(duty*100)

if __name__ == "__main__":
    try:
        dac = PWM_DAC(16, 500, 3.162, True)
        while True:
            try:
                voltage = float(input("Введите напряжение в Вольтах: "))
                dac.set_voltage(voltage)
            except ValueError:
                print("Вы ввели не число. Попробуйте еще раз\n")
    finally:
        dac.deinit()
