import mcp4725_driver as mcp
import signal_generator as sg
import math
import time
import RPi.GPIO as GPIO
import smbus

start = float(time.time())
amp = 3.2
sif = 50
saf = 500


if __name__ == "__main__":
    try:
        dac = mcp.MCP4725(5.0)
        while True:
            try:
                dac.set_voltage((sg.get_sin_wave_amplitude(sif, 2)/2)*amp)
                time.sleep(1/saf)
            except ValueError:
                print('ну ладно...')
    finally:
        dac.deinit()