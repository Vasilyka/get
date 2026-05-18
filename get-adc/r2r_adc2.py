import RPi.GPIO as GPIO
import time
from matplotlib import pyplot as plt
class R2R_ADC:
    def __init__(self, dynamic_range, compare_time=0.01, verbose = False):
        self.dynamic_range= dynamic_range
        self.verbose=verbose
        self.compare_time=compare_time

        self.bits_gpio=[26, 20, 19, 16, 13, 12, 25, 11]
        self.comp_gpio=21
        self.levels = 2**8

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.bits_gpio, GPIO.OUT, initial=0)
        GPIO.setup(self.comp_gpio, GPIO.IN)


    def deinit(self):
            GPIO.output(self.bits_gpio, 0)
            GPIO.cleanup()

    def dec2bin(self, val):
            return [int(e) for e in bin(val)[2:].zfill(8)]
        
    def num2dac(self, val):
            sig = self.dec2bin(val)
            GPIO.output(self.bits_gpio, sig)
            return sig
        
    def seq_count(self):
            for val in range(256):
                self.num2dac(val)
                curvolt = val / 255 *self.dynamic_range
                compVal = GPIO.input(self.comp_gpio)
                time.sleep(self.compare_time)
                if compVal==1:
                    return curvolt
            return curvolt
        
    def suc_approx_adc(self):
            a = -1
            r = 255
            while r-a !=1:
                m = (a+r)//2
                self.num2dac(m)
                time.sleep(self.compare_time)
                if GPIO.input(self.comp_gpio)==1:
                    r = m
                else:
                    a = m
            return r
        
    def get_sar_volt(self):
            return self.suc_approx_adc()/255*self.dynamic_range
if __name__ == "__main__":
    adc = R2R_ADC(3.13, 0.001)
    volts= []
    times =[]
    start_time=time.time()
    try:
        while True:
            print(adc.get_sar_volt())
        """for i in range(100):
            volt = adc.get_sar_volt()
            volts.append(volt)
            print(volt)
            times.append(time.time()-start_time)
            time.sleep(0.03)
        plt.plot(times, volts)
        plt.grid()
        plt.show()
        plt.hist(volts)
        plt.grid()
        plt.show()"""

    finally:
        adc.deinit()