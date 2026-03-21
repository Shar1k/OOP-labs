class TemperatureSensor(Sensor):
    def __init__(self, value=25.0):
        self._value = value
    
    def read_value(self):
        return self._value
    
    @property
    def unit(self):
        return "°C"
    
    def __str__(self):
        return f"Температура: {self._value}{self.unit}"


class PressureSensor(Sensor):
    def __init__(self, value=1.0):
        self._value = value
    
    def read_value(self):
        return self._value
    
    @property
    def unit(self):
        return "psi"
    
    def __str__(self):
        return f"Давление: {self._value} {self.unit}"


class FlowMeter(Sensor):
    def __init__(self, value=100.0):
        self._value = value
    
    def read_value(self):
        return self._value
    
    @property
    def unit(self):
        return "л/мин"
    
    def __str__(self):
        return f"Расход: {self._value} {self.unit}"
    

class BrokenSensor(Sensor):
    def __init__(self, value=10.0):
        self._value = value
    
    @property
    def unit(self):
        return "units"
    
class HumiditySensor(Sensor):
    def __init__(self, value=50.0):
        self._value = value
    
    def read_value(self):
        return self._value
    
    @property
    def unit(self):
        return "%"
    
    def __str__(self):
        return f"Влажность: {self._value}{self.unit}"

