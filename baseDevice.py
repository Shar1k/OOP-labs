from datetime import datetime

class BaseDevice:
    def __init__(self, model, timestamp=None):
        self.__model = model
        self.timestamp = timestamp or datetime.now()
    
    @property
    def model(self):
        return self.__model
    
    @model.setter
    def model(self, value):
        if not isinstance(value, str):
            raise ValueError("Модель должна быть строкой")
        if not value.strip():
            raise ValueError("Модель не может быть пустой")
        self.__model = value
    
    def to_dict(self):
        return {
            'model': self.model,
            'timestamp': self.timestamp.isoformat()
        }
    
    def info(self):
        return f"{self.model}"
    
    def __str__(self):
        return f"Устройство {self.model}"
    
    def __repr__(self):
        return f"BaseDevice('{self.model}')"
    
    def __lt__(self, other):
        if not isinstance(other, BaseDevice):
            return NotImplemented
        return self.model < other.model
    
    def __eq__(self, other):
        if not isinstance(other, BaseDevice):
            return False
        return (type(self) == type(other) and 
                self.model == other.model)