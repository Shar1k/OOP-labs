class VariableFrequencyDrive:
    def __init__(self, model, power, input_voltage, protection_class, frequency_range):
        self.__model = model
        self.__power = power
        self.__input_voltage = input_voltage
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
        min_freq, max_freq = self.output_frequency_range
        if min_freq == 0:
            return "Ошибка (минимальная частота = 0)"
        return max_freq / min_freq
    
    def __str__(self):
        min_freq, max_freq = self.output_frequency_range
        return (f"Частотно-регулируемый привод мощностью {self.__power} кВт.")
    
    def __lt__(self, other):
        return self.__power < other.__power
    
    def __add__(self, other):
        if not isinstance(other, VariableFrequencyDrive):
            raise TypeError(f"Нельзя сложить привод с {type(other).__name__}")
        new_model = f"{self.model} и {other.model}"
        # Мощность - сумма
        new_power = self.power + other.power
        # Напряжение - берем макс
        new_voltage = max(self.__input_voltage, other.__input_voltage)
        # Класс защиты - мин
        new_protection = max(self.protection_class, other.protection_class)
        # Частотный диапазон - самый большой
        new_freq_range = (min(self.output_frequency_range[0], other.output_frequency_range[0]), max(self.output_frequency_range[1], other.output_frequency_range[1]))
        return VariableFrequencyDrive(new_model, new_power, new_voltage, new_protection, new_freq_range)

        
    def __repr__(self):
        min_freq, max_freq = self.output_frequency_range
        return f"VariableFrequencyDrive('{self.__model}', {self.__power}, {min_freq}, {max_freq}, {self.protection_class})"
    
    def __eq__(self, other):
        if not isinstance(other, VariableFrequencyDrive):
            return False
        return self.__model == other.__model

    def info(self):
        min_freq, max_freq = self.output_frequency_range
        return (f"ПЧ {self.__model}: мощность {self.__power} кВт, "
                f"вход {self.__input_voltage} В, "
                f"частота {min_freq}-{max_freq} Гц, "
                f"IP{self.protection_class}")   