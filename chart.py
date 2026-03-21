import matplotlib.pyplot as plt
import random
from datetime import datetime
from fd import VariableFrequencyDrive

def get_current_time():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

powers = []       
frequencies = []   
voltages = []      
times = list(range(1, 11))

for i in range(10):
    power = round(random.uniform(0.5, 100), 1)
    voltage = random.choice([220, 380, 400, 480, 690])
    min_freq = random.choice([0, 0.5, 1, 2, 5])
    max_freq = random.choice([50, 60, 100, 200, 400])
    protection = str(random.choice([20, 21, 54, 55, 65, 66]))
    
    drive = VariableFrequencyDrive(
        model=f"VFD-{random.randint(100, 999)}",
        power=power,
        input_voltage=voltage,
        protection_class=protection,
        frequency_range=(min_freq, max_freq)
    )
    
    powers.append(drive.power)
    frequencies.append(drive.output_frequency_range[1])
    voltages.append(drive.input_voltage)
    
    print(f"  {i+1}. {drive.info()}")


fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))

ax1.plot(times, powers, 'b-o', label='Мощность, кВт', linewidth=3)
ax1.plot(times, frequencies, 'r-s', label='Макс. частота, Гц', linewidth=1)
ax1.set_xlabel('Номер привода')
ax1.set_ylabel('Значение')
ax1.set_title('Параметры частотных приводов')
ax1.grid(True, alpha=0.5)
ax1.legend()

ax2.set_xlabel('Мощность, кВт')
ax2.set_ylabel('Макс. частота, Гц')
ax2.set_title('Зависимость частоты от мощности')
ax2.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('vfd_chart.png', dpi=150)
plt.show()