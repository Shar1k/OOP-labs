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