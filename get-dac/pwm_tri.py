import time
import RPi.GPIO as GPIO

PWM_PIN = 18
PWM_FREQ = 1000
AMP = 3.0          # Амплитуда (В)
FREQ = 2           # Частота треугольника (Гц)
SAMPLING_FREQ = 200

GPIO.setmode(GPIO.BCM)
GPIO.setup(PWM_PIN, GPIO.OUT)
pwm = GPIO.PWM(PWM_PIN, PWM_FREQ)
pwm.start(0)

start_time = time.time()

def get_triangle():
    period = 1.0 / FREQ
    t_mod = (time.time() - start_time) % period
    phase = t_mod / period
    
    if phase < 0.5:
        return phase * 2      # 0 → 1
    else:
        return (1 - phase) * 2 # 1 → 0

def set_voltage_pwm(voltage):
    """Устанавливает напряжение на выходе ШИМ (с ФНЧ)"""
    max_v = 3.3
    if voltage > max_v:
        voltage = max_v
    if voltage < 0:
        voltage = 0
    duty = (voltage / max_v) * 100
    pwm.ChangeDutyCycle(duty)

def wait_for_sampling():
    time.sleep(1.0 / SAMPLING_FREQ)

if __name__ == '__main__':
    try:
        print(f"Треугольник {FREQ} Гц, амплитуда {AMP} В")
        while True:
            tri_val = get_triangle()
            voltage = tri_val * AMP
            set_voltage_pwm(voltage)
            #Для отладки (раскомментируйте):
            print(f"{tri_val:.3f} -> {voltage:.2f} В")
            wait_for_sampling()
    except KeyboardInterrupt:
        print("\nСтоп")
    finally:
        pwm.stop()
        GPIO.cleanup()