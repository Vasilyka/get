import numpy
import time
import math

start = float(time.time())

def get_sin_wave_amplitude(freq, t):
    sin_val = math.sin(2*math.pi*freq*(float(time.time())-start))+1
    return sin_val
def wait(f):
    time.sleep(1/f)