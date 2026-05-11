import pwm_dac as pwm
import signal_generator as sg
import time
import RPi.GPIO as GPIO

amp = 3.2
sif = 2
saf = 1000
start = float(time.time())

GPIO.setmode(GPIO.BCM)
leds = [16,12,25,17,27,23,22,24]
GPIO.setup(leds, GPIO.OUT)
GPIO.output(leds, 0)
dynamic_range=3.3

if __name__ == '__main__':
    try:
        dac = pwm.PWM_DAC(12, 500, dynamic_range, True)
        while True:
            try:
                dac.set_voltage((sg.get_sin_wave_amplitude(sif, 2)/2)*amp)
                time.sleep(1/saf)
            except ValueError:
                print('aaaa')
    finally:
        dac.deinit()