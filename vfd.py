class VariableFrequencyDrive:
    def __init__(self, model, power, input_voltage, protection_class, frequency_range):
        self.__model = model  # приватный атрибут
        self.__power = power  # приватный атрибут
        self.__input_voltage = input_voltage  # приватный атрибут
        self.protection_class = protection_class
        self.output_frequency_range = frequency_range
    
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
        """Вычисляемое свойство: отношение максимальной частоты к минимальной"""
        min_freq, max_freq = self.output_frequency_range
        if min_freq == 0:
            return "Ошибка (минимальная частота = 0)"
        return max_freq / min_freq

    def info(self):
        min_freq, max_freq = self.output_frequency_range
        return (f"ПЧ {self.__model}: мощность {self.__power} кВт, "
                f"вход {self.__input_voltage} В, "
                f"частота {min_freq}-{max_freq} Гц, "
                f"IP{self.protection_class}")