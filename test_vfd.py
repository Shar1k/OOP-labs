import pytest
from datetime import datetime
from vfd import VariableFrequencyDrive
from baseDevice import BaseDevice


class TestVFD:
    """Простые тесты для частотного привода"""
    
    def test_create(self):
        vfd = VariableFrequencyDrive("VFD-007", 7.5, 380, "54", (0, 400))
        
        assert vfd.model == "VFD-007"
        assert vfd.power == 7.5
        assert vfd.input_voltage == 380
        assert vfd.protection_class == "54"
        assert vfd.output_frequency_range == (0, 400)
    
    def test_errors(self):
        vfd = VariableFrequencyDrive("VFD-007", 7.5, 380, "54", (0, 400))
        
        with pytest.raises(ValueError):
            vfd.power = -5         
        
        with pytest.raises(ValueError):
            vfd.power = "строка" 
        
        with pytest.raises(ValueError):
            vfd.input_voltage = -100
    
    def test_speed_range(self):
        vfd1 = VariableFrequencyDrive("VFD-1", 7.5, 380, "54", (0, 50))
        assert vfd1.speed_range == "Ошибка (минимальная частота = 0)"
        
        vfd2 = VariableFrequencyDrive("VFD-2", 7.5, 380, "54", (10, 50))
        assert vfd2.speed_range == 5.0
    
    def test_lt(self):
        small = VariableFrequencyDrive("A", 5.0, 380, "54", (0, 400))
        big = VariableFrequencyDrive("B", 10.0, 380, "54", (0, 400))
        
        assert small < big
        
        drives = [big, small]
        drives.sort()
        assert drives[0] == small
    
    def test_to_dict(self):
        vfd = VariableFrequencyDrive("VFD-007", 7.5, 380, "54", (0, 400))
        data = vfd.to_dict()
        
        assert data['model'] == "VFD-007"
        assert data['power'] == 7.5
        assert 'timestamp' in data


class TestInheritance:
    
    def test_vfd_is_subclass(self):
        """VFD наследуется от BaseDevice"""
        assert issubclass(VariableFrequencyDrive, BaseDevice)
    
    def test_vfd_is_instance(self):
        """Объект VFD является экземпляром BaseDevice"""
        vfd = VariableFrequencyDrive("VFD-007", 7.5, 380, "54", (0, 400))
        assert isinstance(vfd, BaseDevice)
    
    def test_vfd_has_model(self):
        """VFD имеет атрибут model из BaseDevice"""
        vfd = VariableFrequencyDrive("VFD-007", 7.5, 380, "54", (0, 400))
        assert vfd.model == "VFD-007"
    
    def test_constructor_calls_super(self):
        """Конструктор вызывает super()"""
        custom_time = datetime(2024, 1, 1, 12, 0, 0)
        vfd = VariableFrequencyDrive("VFD-007", 7.5, 380, "54", (0, 400), custom_time)
        assert vfd.timestamp == custom_time
    
    def test_to_dict_has_model(self):
        """to_dict() содержит model из BaseDevice"""
        vfd = VariableFrequencyDrive("VFD-007", 7.5, 380, "54", (0, 400))
        data = vfd.to_dict()
        assert 'model' in data