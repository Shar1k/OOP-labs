from datetime import datetime
from baseDevice import BaseDevice


class ElectricMotor(BaseDevice):
    EFFICIENCY_CLASSES = ['IE1', 'IE2', 'IE3', 'IE4', 'IE5']
    MOUNTING_TYPES = ['IM B3', 'IM B5', 'IM B14', 'IM B34', 'IM V1', 'IM V3']
    
    def __init__(self, model, rated_power, rated_speed, efficiency_class, 
                 mounting_type, voltage, timestamp=None):
        super().__init__(model, timestamp)
        
        self.rated_power = rated_power
        self.rated_speed = rated_speed
        self.efficiency_class = efficiency_class
        self.mounting_type = mounting_type
        self.voltage = voltage
    
    @property
    def torque(self):
        return (self.rated_power * 9550) / self.rated_speed
    
    @property
    def pole_pairs(self):
        synchronous_speeds = {3000: 1, 1500: 2, 1000: 3, 750: 4, 600: 5, 500: 6}
        closest_speed = min(synchronous_speeds.keys(), 
                           key=lambda x: abs(x - self.rated_speed))
        return synchronous_speeds[closest_speed]
    
    def validate_number(self, value, name, max_value=None):
        if not isinstance(value, (int, float)):
            raise ValueError(f"{name} должно быть числом")
        if value <= 0:
            raise ValueError(f"{name} должно быть положительным")
        if max_value and value > max_value:
            raise ValueError(f"{name} не может превышать {max_value}")
    
    @property
    def rated_power(self):
        return self._rated_power
    
    @rated_power.setter
    def rated_power(self, value):
        self.validate_number(value, "Номинальная мощность", 5000)
        self._rated_power = value
    
    @property
    def rated_speed(self):
        return self._rated_speed
    
    @rated_speed.setter
    def rated_speed(self, value):
        self.validate_number(value, "Номинальная скорость", 20000)
        self._rated_speed = value
    
    @property
    def efficiency_class(self):
        return self._efficiency_class
    
    @efficiency_class.setter
    def efficiency_class(self, value):
        if value not in self.EFFICIENCY_CLASSES:
            raise ValueError(f"Класс эффективности должен быть одним из: {self.EFFICIENCY_CLASSES}")
        self._efficiency_class = value
    
    @property
    def mounting_type(self):
        return self._mounting_type
    
    @mounting_type.setter
    def mounting_type(self, value):
        if value not in self.MOUNTING_TYPES:
            raise ValueError(f"Тип монтажа должен быть одним из: {self.MOUNTING_TYPES}")
        self._mounting_type = value
    
    @property
    def voltage(self):
        return self._voltage
    
    @voltage.setter
    def voltage(self, value):
        self.validate_number(value, "Напряжение", 15000)
        self._voltage = value
    
    def to_dict(self):
        data = super().to_dict()
        data.update({
            'rated_power': self.rated_power,
            'rated_speed': self.rated_speed,
            'efficiency_class': self.efficiency_class,
            'mounting_type': self.mounting_type,
            'voltage': self.voltage,
            'torque': round(self.torque, 2),
            'pole_pairs': self.pole_pairs
        })
        return data
    
    def info(self):
        return (f"{super().info()}: {self.rated_power} кВт, {self.rated_speed} об/мин, "
                f"{self.efficiency_class}, {self.mounting_type}, {self.voltage} В")
    
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
        return (self.model == other.model &
                abs(self.rated_power - other.rated_power) < 0.001 &
                abs(self.rated_speed - other.rated_speed) < 0.1 &
                self.efficiency_class == other.efficiency_class &
                self.mounting_type == other.mounting_type &
                abs(self.voltage - other.voltage) < 0.1)