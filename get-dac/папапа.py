import RPi.GPIO as GPIO
class PWM_DAC:
    def __init__(self,gpio_pin,pwm_frequency,dynamic_range,verbose=False):
        self.gpio_pin=gpio_pin
        self.dynamic_range=dynamic_range
        self.verbose=verbose
        self.pwm_frequency=pwm_frequency

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.gpio_pin,GPIO.OUT)
        self.pwm=GPIO.PWM(self.gpio_pin,self.pwm_frequency)
        self.pwm.start(0.0)
    def set_number(self,number):
       GPIO.output(self.gpio_pin,[int(element) for element in bin(number)[2:].zfill(8)])
    def set_voltage(self,voltage):
       if not (0.0<=voltage<=self.dynamic_range):
           print(f"Напряжение выходит за динамический диапазон ЦАП (0.00- {self.dynamic_range:.2f} В)")
           print("Устанавливаем 0.0 В")
           return self.pwm.ChangeDutyCycle (0)
       duty=int(voltage/self.dynamic_range*100)
       self.pwm.ChangeDutyCycle(duty)
    def deinit(self):
        GPIO.output(self.gpio_pin,0)
        GPIO.cleanup()
if  __name__=="__main__":
    try:
        dac = PWM_DAC(12,1000,3.183, True)

        while True:
            try:
                voltage=float(input("Введите напряжение в вольтах:"))
                dac.set_voltage(voltage)
            except ValueError:
               print("Вы ввели не число.Попробуйте ещё раз\n")
    finally:
        dac.deinit()
