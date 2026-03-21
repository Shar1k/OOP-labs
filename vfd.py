from datetime import datetime
from baseDevice import BaseDevice

class VariableFrequencyDrive(BaseDevice):
    def __init__(self, model, power, input_voltage, protection_class, 
                 frequency_range, timestamp=None):
        super().__init__(model, timestamp)
        
        self.__power = power
        self.__input_voltage = input_voltage
        self.protection_class = protection_class
        self.output_frequency_range = frequency_range
    
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
    
    def to_dict(self):
        base_dict = super().to_dict()
        min_freq, max_freq = self.output_frequency_range
        base_dict.update({
            'power': self.power,
            'input_voltage': self.input_voltage,
            'protection_class': self.protection_class,
            'min_frequency': min_freq,
            'max_frequency': max_freq,
            'speed_range': self.speed_range
        })
        return base_dict
    
    def __str__(self):
        return f"Привод {self.model} ({self.power} кВт)"
    
    def __repr__(self):
        return (f"VariableFrequencyDrive('{self.model}', {self.power}, "
                f"{self.__input_voltage}, '{self.protection_class}', "
                f"{self.output_frequency_range})")
    
    def __lt__(self, other):
        if not isinstance(other, VariableFrequencyDrive):
            return False
        return self.power < other.power