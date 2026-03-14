from datetime import datetime

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
    
    def to_dict(self):
        min_freq, max_freq = self.output_frequency_range
        return {
            'model': self.model,
            'power': self.power,
            'input_voltage': self.input_voltage,
            'protection_class': self.protection_class,
            'min_frequency': min_freq,
            'max_frequency': max_freq,
            'timestamp': self.timestamp.isoformat(),
            'speed_range': self.speed_range
        }
    
    def info(self):
        min_freq, max_freq = self.output_frequency_range
        return (f"{self.model}: {self.power} кВт, {self.__input_voltage} В, "
                f"{min_freq}-{max_freq} Гц, IP{self.protection_class}")
    
    def __str__(self):
        return f"Привод {self.model} ({self.power} кВт)"
    
    def __repr__(self):
        return (f"VariableFrequencyDrive('{self.model}', {self.power}, "
                f"{self.__input_voltage}, '{self.protection_class}', "
                f"{self.output_frequency_range})")
    
    def __lt__(self, other):
        return self.power < other.power
    
    def __eq__(self, other):
        if not isinstance(other, VariableFrequencyDrive):
            return False
        return (self.model == other.model and
                abs(self.power - other.power) < 0.001 and
                self.__input_voltage == other.__input_voltage and
                self.protection_class == other.protection_class and
                self.output_frequency_range == other.output_frequency_range)