import r2r_dac as r2r
import math
import time
import RPi.GPIO as GPIO
import smbus
import signal_generator as sg


start = float(time.time())
amp = 3.2
sif = 50
saf = 500

class MCP4725:
    def __init__(self, dynamic_range, address=0x61, verbose=True):
        self.bus = smbus.SMBus(1)
        self.address = address
        self.wm = 0x00
        self.pds = 0x00
        self.verbose = verbose
        self.dynamic_range = dynamic_range

    def deinit(self):
        self.bus.close()
    def set_number(self, number):
        if not isinstance(number, int):
            print("Dai celoye chislo")
        elif not (0<=number<=4095):
            print('Out of range (12 bit)')
        else:
            first_byte = self.wm|self.pds|number>>8
            second_byte = number & 0xFF
            self.bus.write_byte_data(0x61, first_byte, second_byte)

            if self.verbose:
                print(f'Chislo: {number}, otpr po I2C: [0x{(self.address<<1):02X}, 0x{first_byte:02X}, 0x{second_byte:02X}]\n')
    
    def set_voltage(self, voltage):
        if not(0.0<=voltage<=self.dynamic_range):
            print('Напряжение за рамками диапазона, сброс до 0.0 В')
        else:
            val = int(voltage/self.dynamic_range*4095)
            self.set_number(val)


if __name__ == "__main__":
    try:
        dac = MCP4725(5.0)
        while True:
            try:
                dac.set_voltage((sg.get_sin_wave_amplitude(sif, 2)/2)*amp)
                time.sleep(1/saf)
            except ValueError:
                print('Вы ввели не число...зачем...')
            except KeyboardInterrupt:
                print('Thank you for using RaspberryPie, bye!')
    finally:
        dac.deinit()