import csv
import json
import random
import os
from datetime import datetime, timedelta

class VariableFrequencyDrive:
    def __init__(self, model, power, input_voltage, protection_class, frequency_range, timestamp=None):
        self.__model = model
        self.__power = power
        self.__input_voltage = input_voltage
        self.protection_class = protection_class
        self.output_frequency_range = frequency_range
        self.timestamp = timestamp or datetime.now()
    
    @property
    def model(self):
        return self.__model
    
    @property
    def power(self):
        return self.__power
    
    @power.setter
    def power(self, value):
        if not isinstance(value, (int, float)):
            raise ValueError("Мощность должна быть числом")
        if value <= 0:
            raise ValueError("Мощность должна быть положительной")
        if value > 1000:
            raise ValueError("Мощность не может превышать 1000 кВт")
        self.__power = value
    
    @property
    def input_voltage(self):
        return self.__input_voltage
    
    @input_voltage.setter
    def input_voltage(self, value):
        if not isinstance(value, (int, float)):
            raise ValueError("Напряжение должно быть числом")
        if value <= 0:
            raise ValueError("Напряжение должно быть положительным")
        if value > 1000:
            raise ValueError("Напряжение не может превышать 1000 В")
        self.__input_voltage = value
    
    @property
    def speed_range(self):
        min_freq, max_freq = self.output_frequency_range
        if min_freq == 0:
            return "Ошибка (минимальная частота = 0)"
        return max_freq / min_freq
    
    def __str__(self):
        return f"Частотно-регулируемый привод {self.__model} мощностью {self.__power} кВт."
    
    def __lt__(self, other):
        return self.__power < other.__power
    
    def __add__(self, other):
        if not isinstance(other, VariableFrequencyDrive):
            raise TypeError(f"Нельзя сложить привод с {type(other).__name__}")
        new_model = f"{self.model} и {other.model}"
        new_power = self.power + other.power
        new_voltage = max(self.__input_voltage, other.__input_voltage)
        new_protection = max(self.protection_class, other.protection_class)
        new_freq_range = (
            min(self.output_frequency_range[0], other.output_frequency_range[0]),
            max(self.output_frequency_range[1], other.output_frequency_range[1])
        )
        new_timestamp = datetime.now()
        return VariableFrequencyDrive(new_model, new_power, new_voltage, new_protection, new_freq_range, new_timestamp)
    
    def __repr__(self):
        min_freq, max_freq = self.output_frequency_range
        return f"VariableFrequencyDrive('{self.__model}', {self.__power}, {self.__input_voltage}, '{self.protection_class}', ({min_freq}, {max_freq}), None)"
    
    def __eq__(self, other):
        if not isinstance(other, VariableFrequencyDrive):
            return False
        return (self.__model == other.__model and
                abs(self.__power - other.__power) < 0.0001 and
                self.__input_voltage == other.__input_voltage and
                self.protection_class == other.protection_class and
                self.output_frequency_range == other.output_frequency_range)


    def info(self):
        min_freq, max_freq = self.output_frequency_range
        return (f"{self.__model}: мощность {self.__power} кВт, "
                f"вход {self.__input_voltage} В, "
                f"частота {min_freq}-{max_freq} Гц, "
                f"IP{self.protection_class}, "
                f"время: {self.timestamp.strftime('%Y-%m-%d %H:%M:%S')}")
    
    @staticmethod
    def generate_test_data(n, **kwargs):
        result = []
        start_date = kwargs.get('start_date', datetime.now())
        time_step = timedelta(days=1)
        
        for i in range(n):
            if 'model' in kwargs:
                model = kwargs['model']
            else:
                model = f"VFD-{random.randint(100, 999)}"
            
            if 'power' in kwargs:
                power = kwargs['power']
            else:
                power = round(random.uniform(0.5, 200), 1)
            
            if 'input_voltage' in kwargs:
                input_voltage = kwargs['input_voltage']
            else:
                input_voltage = random.choice([220, 380, 400, 480, 690])
            
            if 'protection_class' in kwargs:
                protection_class = kwargs['protection_class']
            else:
                protection_class = str(random.choice([20, 21, 54, 55, 65, 66]))
            
            if 'min_freq' in kwargs and 'max_freq' in kwargs:
                min_freq = kwargs['min_freq']
                max_freq = kwargs['max_freq']
            else:
                min_freq = random.choice([0, 0.5, 1, 2, 5])
                max_freq = random.choice([50, 60, 100, 200, 400])
            
            frequency_range = (min_freq, max_freq)
            timestamp = start_date + i * time_step
            
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
    
    def to_dict(self):
        min_freq, max_freq = self.output_frequency_range
        return {
            'model': self.__model,
            'power': self.__power,
            'input_voltage': self.__input_voltage,
            'protection_class': self.protection_class,
            'min_frequency': min_freq,
            'max_frequency': max_freq,
            'timestamp': self.timestamp.isoformat(),
            'speed_range': self.speed_range
        }
    @classmethod
    def from_dict(cls, data):
        timestamp = datetime.fromisoformat(data['timestamp']) if 'timestamp' in data else None
        frequency_range = (data['min_frequency'], data['max_frequency'])
        
        return cls(
            model=data['model'],
            power=data['power'],
            input_voltage=data['input_voltage'],
            protection_class=data['protection_class'],
            frequency_range=frequency_range,
            timestamp=timestamp
        )
    def save_to_csv(filename, data_list):
        if not data_list:
            print("Список пуст, нечего сохранять")
            return
        fieldnames = data_list[0].to_dict().keys()
        
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for drive in data_list:
                writer.writerow(drive.to_dict())
        
        print(f"Данные сохранены в {filename} (CSV, {len(data_list)} записей)")
    
    @staticmethod
    def save_to_csv(filename, data_list):
        if not data_list:
            print("Список пуст, нечего сохранять")
            return
        dict_list = [drive.to_dict() for drive in data_list]
        fieldnames = dict_list[0].keys()
        
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(dict_list)  # Записываем все строки сразу
        
        print(f"Данные сохранены в {filename} (CSV, {len(data_list)} записей)")
    
    @staticmethod
    def save_to_json(filename, data_list):
        if not data_list:
            print("Список пуст, нечего сохранять")
            return
        json_data = [drive.to_dict() for drive in data_list]
        
        with open(filename, 'w', encoding='utf-8') as jsonfile:
            json.dump(json_data, jsonfile, ensure_ascii=False, indent=2)
        
        print(f"Данные сохранены в {filename} (JSON, {len(data_list)} записей)")
    
    @staticmethod
    def load_from_csv(filename):
        drives = []
        with open(filename, 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                row['power'] = float(row['power'])
                row['input_voltage'] = int(float(row['input_voltage']))
                row['min_frequency'] = float(row['min_frequency'])
                row['max_frequency'] = float(row['max_frequency'])
                drive = VariableFrequencyDrive.from_dict(row)
                drives.append(drive)
        
        print(f"Загружено {len(drives)} записей из {filename}")
        return drives
    
    @staticmethod
    def load_from_json(filename):
        with open(filename, 'r', encoding='utf-8') as jsonfile:
            json_data = json.load(jsonfile)
        
        drives = [VariableFrequencyDrive.from_dict(item) for item in json_data]
        print(f"Загружено {len(drives)} записей из {filename}")
        return drives