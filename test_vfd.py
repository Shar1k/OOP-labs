import pytest
from vfd import VariableFrequencyDrive

#Создание объекта
def test_create():
    vfd = VariableFrequencyDrive("VFD-007", 7.5, 380, "54", (0, 400))
    
    assert vfd.model == "VFD-007"
    assert vfd.power == 7.5
    assert vfd.input_voltage == 380
    assert vfd.protection_class == "54"
    assert vfd.output_frequency_range == (0, 400)


#Проверка ошибок
def test_errors():
    vfd = VariableFrequencyDrive("VFD-007", 7.5, 380, "54", (0, 400))
    
    # Должны быть ошибки
    with pytest.raises(ValueError):
        vfd.power = -5         
    
    with pytest.raises(ValueError):
        vfd.power = "строка" 
    
    with pytest.raises(ValueError):
        vfd.input_voltage = -100 


#Вычисляемое свойство
def test_speed():

    vfd1 = VariableFrequencyDrive("VFD-1", 7.5, 380, "54", (0, 50))
    assert vfd1.speed_range == "Ошибка (минимальная частота = 0)"
    
    vfd2 = VariableFrequencyDrive("VFD-2", 7.5, 380, "54", (10, 50))
    assert vfd2.speed_range == 5.0


#Сравнение
def test_eq():
    vfd1 = VariableFrequencyDrive("VFD-007", 7.5, 380, "54", (0, 400))
    vfd2 = VariableFrequencyDrive("VFD-007", 7.5, 380, "54", (0, 400))
    vfd3 = VariableFrequencyDrive("VFD-008", 12, 220, "77", (100, 300)) 
    
    assert vfd1 == vfd2      
    assert vfd1 != vfd3      
    assert vfd1 != "строка"  


def test_lt():
    small = VariableFrequencyDrive("A", 5.0, 380, "54", (0, 400))
    big = VariableFrequencyDrive("B", 10.0, 380, "54", (0, 400))
    
    assert small > big
    assert not (big < small)
    
    list = [big, small]
    list.sort()
    assert list[0] == small 


def test_add():
    vfd1 = VariableFrequencyDrive("VFD-1", 7.5, 380, "54", (0, 400))
    vfd2 = VariableFrequencyDrive("VFD-2", 11.0, 400, "65", (5, 500))
    
    res = vfd1 + vfd2
    assert res.model == "VFD-1 и VFD-2"
    assert res.power == 18.5           
    assert res.input_voltage == 400    
    assert res.protection_class == "65" 
    assert res.output_frequency_range == (0, 500)
    
    with pytest.raises(TypeError):
        vfd1 + "строка"