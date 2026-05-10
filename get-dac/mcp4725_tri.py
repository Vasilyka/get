import mcp4725_driver as mcp
import time
import math

amp = 3.2           # Амплитуда сигнала (Вольт, от 0 до amp)
freq = 2            # Частота треугольного сигнала (Гц)
sampling_freq = 200 # Частота дискретизации (Гц)

start_time = time.time()

def get_triangle(freq):
    """
    Возвращает значение треугольной волны в диапазоне 0..1
    """
    period = 1.0 / freq
    t_mod = (time.time() - start_time) % period
    phase = t_mod / period
    
    if phase < 0.5:
        # Подъём: 0 → 1
        return phase * 2
    else:
        # Спад: 1 → 0
        return (1 - phase) * 2

if __name__ == "__main__":
    try:
        dac = mcp.MCP4725(5.0)
        print(f"Треугольный сигнал: {freq} Гц, амплитуда {amp} В")
        print(f"Дискретизация: {sampling_freq} Гц")
        
        while True:
            tri_norm = get_triangle(freq)
            voltage = tri_norm * amp
            dac.set_voltage(voltage)
            time.sleep(1 / sampling_freq)
            
    except KeyboardInterrupt:
        print("\nОстановлено")
    finally:
        dac.deinit()