import smbus
import time

class MCP4725_DAC:
    def __init__(self, address=0x61, verbose=True):
        self.bus = smbus.SMBus(1)
        self.address = address
        self.verbose = verbose
        self.real_max_voltage = None
        self.calibration_factor = 1.0
        self._auto_calibrate()
    
    def _auto_calibrate(self):
        """Автоматическая калибровка с учётом реального выхода"""
        print("\n=== АВТОКАЛИБРОВКА ЦАП ===")
        
        # 1. Устанавливаем максимальный код
        max_code = 4095
        self._raw_write(max_code)
        time.sleep(0.5)
        
        # 2. Просим пользователя измерить
        print(f"\n1. Установлен код {max_code} (максимум)")
        print("2. ИЗМЕРЬТЕ мультиметром напряжение на выходе ЦАП")
        
        while True:
            try:
                measured = float(input("3. Введите измеренное напряжение (В): "))
                if 0 < measured <= 5.5:
                    break
                print("Напряжение должно быть от 0 до 5.5 В")
            except ValueError:
                print("Введите число")
        
        # 3. Рассчитываем реальный максимум
        # Если при коде 4095 получили 4.2 В, значит реальный максимум = 4.2 В
        self.real_max_voltage = measured
        
        # 4. Коэффициент нелинейности (если нужно)
        theoretical = 5.3  # ваш изначальный dynamic_range
        self.calibration_factor = measured / theoretical
        
        print(f"\n✅ Калибровка завершена!")
        print(f"   Реальный максимум: {self.real_max_voltage:.3f} В")
        print(f"   Коэффициент коррекции: {self.calibration_factor:.3f}")
        print(f"   Ошибка: {(1 - self.calibration_factor)*100:.1f}%\n")
    
    def _raw_write(self, number):
        """Непосредственная запись в ЦАП"""
        first_byte = 0x60 | (number >> 8)
        second_byte = number & 0xFF
        self.bus.write_byte_data(self.address, first_byte, second_byte)
    
    def set_voltage(self, voltage):
        """Установка напряжения с учётом калибровки"""
        if voltage < 0:
            voltage = 0
        if voltage > self.real_max_voltage:
            print(f"Предупреждение: {voltage:.2f} В выше максимума ({self.real_max_voltage:.2f} В)")
            voltage = self.real_max_voltage
        
        # Корректируем напряжение перед расчётом кода
        # Если хотим 3.0 В, а реальный максимум 4.2 В, то код = 3.0 / 4.2 * 4095
        code = int(round((voltage / self.real_max_voltage) * 4095))
        code = max(0, min(4095, code))
        
        self._raw_write(code)
        
        if self.verbose:
            expected = self.voltage_from_code(code)
            print(f"Запрошено: {voltage:.3f} В → Код: {code} → Ожидается: {expected:.3f} В")
        
        return expected
    
    def voltage_from_code(self, code):
        """По коду получаем реальное напряжение"""
        return code / 4095.0 * self.real_max_voltage
    
    def deinit(self):
        self.bus.close()

# Расширенная версия с автоматической подстройкой
class AutoCalibratingMCP4725(MCP4725_DAC):
    def __init__(self, address=0x61, verbose=True):
        super().__init__(address, verbose)
        self.load_calibration()
    
    def load_calibration(self):
        """Загружает калибровку из файла"""
        try:
            with open('dac_calibration.txt', 'r') as f:
                self.real_max_voltage = float(f.read().strip())
                print(f"Загружена калибровка: {self.real_max_voltage:.3f} В")
        except FileNotFoundError:
            self._auto_calibrate()
            self.save_calibration()
    
    def save_calibration(self):
        """Сохраняет калибровку в файл"""
        with open('dac_calibration.txt', 'w') as f:
            f.write(str(self.real_max_voltage))
        print("Калибровка сохранена")

if __name__ == "__main__":
    # Вариант 1: Простая калибровка
    dac = MCP4725_DAC()
    
    # Вариант 2: С автокалибровкой (раскомментировать)
    # dac = AutoCalibratingMCP4725()
    
    try:
        print("\n=== ТЕСТИРОВАНИЕ ===")
        
        # Тест: устанавливаем разные напряжения
        test_voltages = [0, 1.0, 2.0, 3.0, 4.0, dac.real_max_voltage]
        
        for v in test_voltages:
            print(f"\n--- Установка {v:.2f} В ---")
            dac.set_voltage(v)
            time.sleep(2)  # Даём время измерить мультиметром
            input("Измерьте напряжение и нажмите Enter...")
        
        # Интерактивный режим
        print(f"\n=== ИНТЕРАКТИВНЫЙ РЕЖИМ ===")
        print(f"Диапазон: 0 - {dac.real_max_voltage:.3f} В")
        
        while True:
            try:
                v = float(input("\nВведите напряжение (В): "))
                dac.set_voltage(v)
            except ValueError:
                print("Введите число")
            except KeyboardInterrupt:
                print("\nВыход")
                break
    
    finally:
        dac.deinit()