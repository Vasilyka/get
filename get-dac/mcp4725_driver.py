import smbus
import time

class MCP4725_DAC:
    def __init__(self, address=0x61, verbose=True):
        self.bus = smbus.SMBus(1)
        self.address = address
        self.verbose = verbose
        self.real_max_voltage = None
        self._calibrate()
    
    def _calibrate(self):
        """Автоматически определяет реальное максимальное напряжение"""
        print("Калибровка ЦАП...")
        
        # Устанавливаем максимальный код (4095)
        first_byte = 0x60 | (4095 >> 8)  # Быстрая запись без EEPROM
        second_byte = 4095 & 0xFF
        
        try:
            self.bus.write_byte_data(self.address, first_byte, second_byte)
            time.sleep(0.1)
            
            # Читаем регистр конфигурации (опционально)
            config = self.bus.read_byte_data(self.address, 0x00)
            
            print("\n*** ИЗМЕРЬТЕ МУЛЬТИМЕТРОМ НАПРЯЖЕНИЕ НА ВЫХОДЕ ЦАП ***")
            print("И введите его в вольтах (например, 4.2):")
            
            while self.real_max_voltage is None:
                try:
                    self.real_max_voltage = float(input("Реальное макс. напряжение: "))
                    if self.real_max_voltage <= 0:
                        print("Введите положительное число")
                        continue
                    break
                except ValueError:
                    print("Ошибка: введите число")
            
            print(f"Калибровка завершена. Реальный максимум: {self.real_max_voltage:.3f} В")
            
        except OSError as e:
            print(f"Ошибка при калибровке: {e}")
            self.real_max_voltage = 4.2  # Значение по умолчанию
            print(f"Установлен максимум по умолчанию: {self.real_max_voltage} В")
    
    def set_voltage(self, voltage):
        if self.real_max_voltage is None:
            print("Ошибка: ЦАП не откалиброван")
            return False
        
        if not (0.0 <= voltage <= self.real_max_voltage):
            print(f"Ошибка: {voltage:.2f} В вне диапазона (0-{self.real_max_voltage:.2f} В)")
            return False
        
        # Корректная формула с округлением
        number = int(round((voltage / self.real_max_voltage) * 4095))
        number = max(0, min(4095, number))  # Защита от выхода за пределы
        
        return self._write_number(number)
    
    def _write_number(self, number):
        first_byte = 0x60 | (number >> 8)
        second_byte = number & 0xFF
        
        try:
            self.bus.write_byte_data(self.address, first_byte, second_byte)
            if self.verbose:
                print(f"Установлено: {self._number_to_voltage(number):.3f} В (код {number})")
            return True
        except OSError as e:
            print(f"Ошибка записи I2C: {e}")
            return False
    
    def _number_to_voltage(self, number):
        return number / 4095.0 * self.real_max_voltage
    
    def deinit(self):
        self.bus.close()

if __name__ == "__main__":
    dac = MCP4725_DAC()
    
    try:
        while True:
            try:
                voltage = float(input(f"\nВведите напряжение (0 - {dac.real_max_voltage:.2f} В): "))
                dac.set_voltage(voltage)
            except ValueError:
                print("Введите число")
            except KeyboardInterrupt:
                print("\nВыход")
                break
    finally:
        dac.deinit()