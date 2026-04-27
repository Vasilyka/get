import r2r_dac as r2r
import signal_generator as sg
import time
import RPi.GPIO as GPIO

amp = 3.2
sif = 10
saf = 1000
leds = [16, 20, 21, 25, 26, 17, 27, 22]
dynamic_range = 3.14
start = float(time.time())

if __name__ == '__main__':
    try:
        dac = r2r.R2R_DAC(leds, dynamic_range, True)
        while True:
            try:
                dac.set_voltage((sg.get_sin_wave_amplitude(sif, 2)/2)*amp)
                sg.wait_for_sampling_period(saf)
            except ValueError:
                print('aaaa')
    finally:
        dac.deinit()