from baseDevice import BaseDevice

class ElectricMotor(BaseDevice):
    EFFICIENCY_CLASSES = ['IE1', 'IE2', 'IE3', 'IE4', 'IE5']
    
    def __init__(self, model, rated_power, rated_speed, efficiency_class, 
                 mounting_type, voltage, timestamp=None):
        super().__init__(model, timestamp)
        
        self.__rated_power = rated_power
        self.__rated_speed = rated_speed
        self.efficiency_class = efficiency_class
        self.mounting_type = mounting_type
        self.voltage = voltage
    
    @property
    def rated_power(self):
        return self.__rated_power
    
    @rated_power.setter
    def rated_power(self, value):
        if not isinstance(value, (int, float)):
            raise ValueError("Номинальная мощность должна быть числом")
        if value <= 0:
            raise ValueError("Номинальная мощность должна быть положительной")
        if value > 5000:
            raise ValueError("Номинальная мощность не может превышать 5000 кВт")
        self.__rated_power = value
    
    @property
    def rated_speed(self):
        return self.__rated_speed
    
    @rated_speed.setter
    def rated_speed(self, value):
        if not isinstance(value, (int, float)):
            raise ValueError("Номинальная скорость должна быть числом")
        if value <= 0:
            raise ValueError("Номинальная скорость должна быть положительной")
        if value > 20000:
            raise ValueError("Номинальная скорость не может превышать 20000 об/мин")
        self.__rated_speed = value
    
    @property
    def torque(self):
        return (self.__rated_power * 9550) / self.__rated_speed
    
    @property
    def pole_pairs(self):
        synchronous_speeds = {3000: 1, 1500: 2, 1000: 3, 750: 4, 600: 5, 500: 6}
        closest_speed = min(synchronous_speeds.keys(), 
                           key=lambda x: abs(x - self.__rated_speed))
        return synchronous_speeds[closest_speed]
    
    @property
    def efficiency_class(self):
        return self.__efficiency_class
    
    @efficiency_class.setter
    def efficiency_class(self, value):
        if value not in self.EFFICIENCY_CLASSES:
            raise ValueError(f"Класс эффективности должен быть одним из: {self.EFFICIENCY_CLASSES}")
        self.__efficiency_class = value
    
    @property
    def mounting_type(self):
        return self.__mounting_type
    
    @mounting_type.setter
    def mounting_type(self, value):
        valid_types = ['IM B3', 'IM B5', 'IM B14', 'IM B34', 'IM V1', 'IM V3']
        if value not in valid_types:
            raise ValueError(f"Тип монтажа должен быть одним из: {valid_types}")
        self.__mounting_type = value
    
    @property
    def voltage(self):
        return self.__voltage
    
    @voltage.setter
    def voltage(self, value):
        if not isinstance(value, (int, float)):
            raise ValueError("Напряжение должно быть числом")
        if value <= 0:
            raise ValueError("Напряжение должно быть положительным")
        if value > 15000:
            raise ValueError("Напряжение не может превышать 15000 В")
        self.__voltage = value
    
    def to_dict(self):
        base_dict = super().to_dict()
        base_dict.update({
            'rated_power': self.rated_power,
            'rated_speed': self.rated_speed,
            'efficiency_class': self.efficiency_class,
            'mounting_type': self.mounting_type,
            'voltage': self.voltage,
            'torque': round(self.torque, 2),
            'pole_pairs': self.pole_pairs
        })
        return base_dict
    
    def info(self):
        base_info = super().info()
        return (f"{base_info}: {self.rated_power} кВт, {self.rated_speed} об/мин, "
                f"{self.efficiency_class}, {self.mounting_type}, {self.voltage} В, "
                f"Момент: {self.torque:.1f} Нм")
    
    def start(self):
        return f"Двигатель {self.model} запущен. Номинальная скорость: {self.rated_speed} об/мин"
    
    def stop(self):
        return f"Двигатель {self.model} остановлен"
    
    def __str__(self):
        return f"Электродвигатель {self.model} ({self.rated_power} кВт)"
    
    def __repr__(self):
        return (f"ElectricMotor('{self.model}', {self.rated_power}, "
                f"{self.rated_speed}, '{self.efficiency_class}', "
                f"'{self.mounting_type}', {self.voltage})")
    
    def __lt__(self, other):
        if not isinstance(other, ElectricMotor):
            return NotImplemented
        return self.rated_power < other.rated_power
    
    def __eq__(self, other):
        if not isinstance(other, ElectricMotor):
            return False
        return (super().__eq__(other) and
                abs(self.rated_power - other.rated_power) < 0.001 and
                abs(self.rated_speed - other.rated_speed) < 0.1 and
                self.efficiency_class == other.efficiency_class and
                self.mounting_type == other.mounting_type and
                abs(self.voltage - other.voltage) < 0.1)
    
    def __gt__(self, other):
        if not isinstance(other, ElectricMotor):
            return NotImplemented
        return self.rated_power > other.rated_power