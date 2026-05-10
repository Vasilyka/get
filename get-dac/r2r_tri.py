import r2r_dac as r2r
import time
import RPi.GPIO as GPIO

amp = 3.2
sif = 10
saf = 1000
leds = [16,20,21,25,26,17,27,22]
dynamic_range = 3.14
start = float(time.time())

for pin in leds:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)

def set_val(val):
    for i, pin in enumerate((leds)):
        GPIO.output(pin, (val>>(7-i))&1)
try:
    while True:
        for value in range(256):
            set_val(value)
            time.sleep(0.001)
        for value in range(254, 1, -1):
            set_val(value)
            time.sleep(0.001)
except KeyboardInterrupt:
    set_val(0)
    GPIO.cleanup()


"""

import time
import math
import RPi.GPIO as GPIO
import r2r_dac as r2r

AMP = 3.2          # Амплитуда (Вольт, макс. значение)
FREQ = 2           # Частота (Герц)
SAMPLING_FREQ = 200 # Частота дискретизации (Гц) — чем выше, тем глаже сигнал

leds = [16, 20, 21, 25, 26, 17, 27, 22]
dynamic_range = 3.162

start_time = time.time()

def get_triangle(freq):
    period = 1.0 / freq
    t_mod = (time.time() - start_time) % period
    phase = t_mod / period
    
    if phase < 0.5:
        return phase * 4      # 0 → 2
    else:
        return (1 - phase) * 4 # 2 → 0

if __name__ == '__main__':
    try:
        dac = r2r.R2R_DAC(leds, dynamic_range, True)
        print(f"Треугольный сигнал: {FREQ} Гц, амплитуда {AMP} В")
        print(f"Дискретизация: {SAMPLING_FREQ} Гц")
        
        while True:
            triangle_val = get_triangle(FREQ)
            voltage = (triangle_val / 2) * AMP
            dac.set_voltage(voltage)
            time.sleep(1.0 / SAMPLING_FREQ)
            
    except KeyboardInterrupt:
        print("\nОстановлено")
    finally:
        dac.deinit()

"""