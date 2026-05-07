import smbus

class MCP4725:
    def __init__(self, dynamic_range, address=0x61, verbose=True):
        self.bus = smbus.SMBus(1)
        self.address = address
        self.verbose = verbose
        self.dynamic_range = dynamic_range

    def deinit(self):
        self.bus.close()
    
    def set_number(self, number):
        if not isinstance(number, int):
            print("На вход ЦАП можно подавать только целые числа")
            return
        if not (0 <= number <= 4095):
            print('Число выходит за разрядность MCP4725 (12 бит)')
            return
        
        # Правильное формирование first_byte:
        # Команда 0x60 = 0b01100000 (запись в EEPROM с быстрым режимом)
        # Или 0x40 = 0b01000000 (только быстрый режим, без EEPROM)
        command = 0x60  # 0x60 - запись в EEPROM и выход, 0x40 - только выход
        
        # Берем старшие 4 бита числа (D11, D10, D9, D8)
        # но MCP4725 ожидает в first_byte: [C2,C1,C0,PD1,PD0, D11,D10,D9]
        # Т.е. только 3 старших бита, а D8 в second_byte!
        first_byte = command | ((number >> 8) & 0x0F)  # правильный сдвиг
        second_byte = number & 0xFF
        
        # Отправляем данные
        self.bus.write_i2c_block_data(self.address, first_byte, [second_byte])
        
        if self.verbose:
            print(f'Число: {number}, отправленные данные: [0x{first_byte:02X}, 0x{second_byte:02X}]')
    
    def set_voltage(self, voltage):
        if not (0.0 <= voltage <= self.dynamic_range):
            print(f'Напряжение {voltage:.2f} В за рамками диапазона (0.00 - {self.dynamic_range:.2f} В), сброс до 0.0 В')
            self.set_number(0)
        else:
            val = int(voltage / self.dynamic_range * 4095)
            if self.verbose:
                expected = val / 4095 * self.dynamic_range
                print(f'Запрошено {voltage:.3f} В → число {val} → ожидается ~{expected:.3f} В')
            self.set_number(val)

if __name__ == "__main__":
    try:
        # ВАЖНО: укажите реальное напряжение питания MCP4725!
        # Измерьте мультиметром напряжение на пине VDD микросхемы
        dac = MCP4725(5.0, 0x61, True)  # если питание 5 В
        # dac = MCP4725(3.3, 0x61, True)  # если питание 3.3 В
        
        while True:
            try:
                voltage = float(input('Введите напряжение в Вольтах: '))
                dac.set_voltage(voltage)
            except ValueError:
                print('Вы ввели не число. Попробуйте ещё раз')
    except KeyboardInterrupt:
        print('\nПрограмма завершена')
    finally:
        dac.deinit()