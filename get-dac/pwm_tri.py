import r2r_dac as r2r
import signal_generator as sg
import time
import RPi.GPIO as GPIO
import smbus
amp = 3.2
sif = 10
saf = 1000
leds = [16,20,21,25,26,17,27,22]
dynamic_range=3.14
start = float(time.time())

class Triag:
    def __init__(self, led=12, F=200, v=1, f=0.05):
        GPIO.setmode(GPIO.BCM)
        self.led=led
        self.step=v
        self.tim=1/f
        self.f=F
        GPIO.setup(led, GPIO.OUT)
        pwm=GPIO.PWM(self.led, self.f)
        duty=0.0
        pwm.start(duty)
        while True:
            pwm.ChangeDutyCycle(duty)
            time.sleep(self.step)
            duty+=self.step
            if duty>=100.0 or duty<=0.0:
                self.step=-self.step


if __name__ == '__main__':
    try:
        print(f"Треугольник {FREQ} Гц, амплитуда {AMP} В")
        while True:
            tri_val = get_triangle()
            voltage = tri_val * AMP
            set_voltage_pwm(voltage)
            # Для отладки (раскомментируйте):
            # print(f"{tri_val:.3f} -> {voltage:.2f} В")
            wait_for_sampling()
    except KeyboardInterrupt:
        print("\nСтоп")
    finally:
        dac.deinit()