import random
from datetime import datetime, timedelta
from fd import VariableFrequencyDrive

def from_dict(data):
    timestamp = datetime.fromisoformat(data['timestamp']) if 'timestamp' in data else None
    frequency_range = (float(data['min_frequency']), float(data['max_frequency']))
    
    return VariableFrequencyDrive(
        model=data['model'],
        power=float(data['power']),
        input_voltage=int(float(data['input_voltage'])),
        protection_class=data['protection_class'],
        frequency_range=frequency_range,
        timestamp=timestamp
    )

def generate_test_data(n, **kwargs):
    result = []
    
    start_date = kwargs.get('start_date', datetime.now())
    time_step = timedelta(days=1)
    
    for i in range(n):
        # Модель
        if 'model' in kwargs:
            model = kwargs['model']
        else:
            model = f"VFD-{random.randint(100, 999)}"
        
        # Мощность
        if 'power' in kwargs:
            power = kwargs['power']
        else:
            power = round(random.uniform(0.5, 200), 1)
        
        # Напряжение
        if 'input_voltage' in kwargs:
            input_voltage = kwargs['input_voltage']
        else:
            input_voltage = random.choice([220, 380, 400, 480, 690])
        
        # Класс защиты
        if 'protection_class' in kwargs:
            protection_class = kwargs['protection_class']
        else:
            protection_class = str(random.choice([20, 21, 54, 55, 65, 66]))
        
        # Диапазон частот
        if 'min_freq' in kwargs and 'max_freq' in kwargs:
            min_freq = kwargs['min_freq']
            max_freq = kwargs['max_freq']
        else:
            min_freq = random.choice([0, 0.5, 1, 2, 5])
            max_freq = random.choice([50, 60, 100, 200, 400])
        
        frequency_range = (min_freq, max_freq)
        
        # Временная метка с равномерным шагом
        timestamp = start_date + i * time_step
        
        # Создаем объект
        drive = VariableFrequencyDrive(
            model=model,
            power=power,
            input_voltage=input_voltage,
            protection_class=protection_class,
            frequency_range=frequency_range,
            timestamp=timestamp
        )
        
        result.append(drive)
    
    return result