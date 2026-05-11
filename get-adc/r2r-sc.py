import time
import r2r_adc2
import adc_plot
from matplotlib import pyplot as plt
adc = r2r_adc2.R2R_ADC(3.143, 0.0007)
volts = []
times = []
dur = 3.0
try:
    start = time.time()
    for i in range(100):
            volt = adc.get_sar_volt()
            volts.append(volt)
            print(volt)
            times.append(time.time()-start)
            time.sleep(0.03)
    plt.plot(times, volts)
    plt.grid()
    plt.show()
    plt.hist(volts)
    plt.grid()
    plt.show()
finally:
    adc.deinit()