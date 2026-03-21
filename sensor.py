from abc import ABC, abstractmethod


class Sensor(ABC):
    
    @abstractmethod
    def read_value(self):
        pass
    
    @property
    @abstractmethod
    def unit(self):
        pass

    def description(self):
        return f"Класс - {self.__class__.__name__}, ед. измерения {self.unit}"
    
    