import RPi.GPIO as GPIO
import time

class R2R_ADC:
    def __init__(self, dynamic_range, compare_time = 0.01, verbose = False):
        self.dynamic_range = dynamic_range
        self.verbose = verbose
        self.compare_time = compare_time
        
        self.bits_gpio = [26, 20, 19, 16, 13, 12, 25, 11]
        self.comp_gpio = 21
        self.levels = 2**8

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.bits_gpio, GPIO.OUT, initial = 0)
        GPIO.setup(self.comp_gpio, GPIO.IN)

    def deinit(self):
        GPIO.output(self.bits_gpio, 0)
        GPIO.cleanup()

    def dec2bin(self, value):
        return [int(element) for element in bin(value)[2:].zfill(8)]

    def num2dac(self, value):
        signal = self.dec2bin(value)
        GPIO.output(self.bits_gpio, signal)
        return signal

    def sequential_counting_adc(self):
        for value in range(256):
            signal = self.num2dac(value)
            voltage = value / self.levels * self.dynamic_range
            comparatorValue = GPIO.input(self.comp_gpio)
            time.sleep(self.compare_time)
            if comparatorValue == 1:
                return voltage
        return voltage

    def successive_approximation_adc(self):
        a = -1
        r = 255
        while r-a != 1:
            m = (a+r)//2
            self.num2dac(m)
            time.sleep(self.compare_time)
            if GPIO.input(self.comp_gpio) == 1:
                r = m
            else:
                a = m
        return r
    def get_sar_voltage(self):
        return self.successive_approximation_adc() / 255 * self.dynamic_range

if __name__ == "__main__":
    try:
        adc = R2R_ADC(3.13, 0.001)
        
        while True:
            print(adc.sequential_counting_adc())
            #print(adc.get_sar_voltage())
    finally:
        adc.deinit()