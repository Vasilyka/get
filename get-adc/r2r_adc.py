import RPi.GPIO as GPIO
import time 
def dec2bin(value):
    return [int(element) for element in bin(value)[2:].zfill(8)]

class R2R_ADC:
    def __init__(self, dynamic_range, compare_time = 0.001, verbose = False):
        self.dynamic_range = dynamic_range
        self.verbose = verbose
        self.compare_time = compare_time

        self.bits_gpio = [26, 20, 19, 16, 13, 12, 25, 11]
        self.comp_gpio = 21

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.bits_gpio, GPIO.OUT, initial = 0)
        GPIO.setup(self.comp_gpio, GPIO.IN)

    def deinit(self):
        GPIO.output(self.bits_gpio, 0)
        GPIO.cleanup()

    def number_to_dac(self, number):
        num = dec2bin(number)
        GPIO.output(self.bits_gpio, num)

    def sequential_counting_adc(self):
        for val in range(255+1):
            self.number_to_dac(val)
            time.sleep(self.compare_time)
            comp = GPIO.input(self.comp_gpio)
            if comp == 1:
                    return val
        return 255

    def get_sc_voltage(self):
        #volt = (self.sequential_counting_adc() / 255) * self.dynamic_range
        #GPIO.output(self.bits_gpio, self.sequential_counting_adc())
        #return volt
        val = self.sequential_counting_adc()
        GPIO.output(self.bits_gpio, val)
        return (val/256) * self.dynamic_range

if __name__ == "__main__":
    dac = None
    try:
        dac = R2R_ADC(3.23)
        while True:
            print(dac.get_sc_voltage())
    finally:
        dac.deinit()