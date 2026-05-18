# Измерьте реальный максимум один раз (например, 4.2 В)
REAL_MAX = 4.2  # Подставьте ваше измеренное значение

class MCP4725_DAC:
    def __init__(self, dynamic_range, address=0x61, verbose=True):
        self.bus = smbus.SMBus(1)
        self.address = address
        self.wm = 0x00
        self.pds = 0x00
        self.verbose = verbose
        self.dynamic_range = dynamic_range
        self.real_max = REAL_MAX  # Реальный максимум после калибровки
    
    def set_voltage(self, voltage):
        if not (0.0 <= voltage <= self.dynamic_range):
            print(f"Напряжение {voltage} вне диапазона (0-{self.dynamic_range})")
            return 0
        
        # ИСПРАВЛЕННАЯ ФОРМУЛА с учётом реального максимума
        number = int(voltage / self.real_max * 4095)
        number = min(4095, max(0, number))
        self.set_number(number)
    
    # ... остальной код без изменений