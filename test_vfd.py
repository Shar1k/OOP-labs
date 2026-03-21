import pytest
from datetime import datetime
from fd import VariableFrequencyDrive

def test_create():
    vfd = VariableFrequencyDrive("VFD-007", 7.5, 380, "54", (0, 400))
    
    assert vfd.model == "VFD-007"
    assert vfd.power == 7.5
    assert vfd.input_voltage == 380
    assert vfd.protection_class == "54"
    assert vfd.output_frequency_range == (0, 400)
    assert isinstance(vfd.timestamp, datetime)

def test_errors():
    vfd = VariableFrequencyDrive("VFD-007", 7.5, 380, "54", (0, 400))
    
    with pytest.raises(ValueError, match="Мощность должна быть положительной"):
        vfd.power = -5         
    
    with pytest.raises(ValueError, match="Мощность должна быть числом"):
        vfd.power = "строка" 
    
    with pytest.raises(ValueError, match="Напряжение должно быть положительным"):
        vfd.input_voltage = -100
    
    with pytest.raises(ValueError, match="Мощность не может превышать 1000 кВт"):
        vfd.power = 1500

def test_speed_range():
    vfd1 = VariableFrequencyDrive("VFD-1", 7.5, 380, "54", (0, 50))
    assert vfd1.speed_range == "Ошибка (минимальная частота = 0)"
    
    vfd2 = VariableFrequencyDrive("VFD-2", 7.5, 380, "54", (10, 50))
    assert vfd2.speed_range == 5.0

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
    
    assert small < big
    assert not (big < small)
    
    drives = [big, small]
    drives.sort()
    assert drives[0] == small


def test_add():
    vfd1 = VariableFrequencyDrive("VFD-1", 7.5, 380, "54", (0, 400))
    vfd2 = VariableFrequencyDrive("VFD-2", 11.0, 400, "65", (5, 500))
    
    result = vfd1 + vfd2
    assert result.model == "VFD-1 и VFD-2"
    assert result.power == 18.5           
    assert result.input_voltage == 400    
    assert result.protection_class == "65" 
    assert result.output_frequency_range == (0, 500)
    
    with pytest.raises(TypeError, match="Нельзя сложить привод с str"):
        vfd1 + "строка"

def test_to_dict():
    vfd = VariableFrequencyDrive("VFD-007", 7.5, 380, "54", (0, 400))
    data = vfd.to_dict()
    
    assert data['model'] == "VFD-007"
    assert data['power'] == 7.5
    assert data['input_voltage'] == 380
    assert data['protection_class'] == "54"
    assert data['min_frequency'] == 0
    assert data['max_frequency'] == 400
    assert 'timestamp' in data
    assert 'speed_range' in data

def test_from_dict():
    original = VariableFrequencyDrive("VFD-007", 7.5, 380, "54", (0, 400))
    data = original.to_dict()
    restored = VariableFrequencyDrive.from_dict(data)
    
    assert original == restored
def test_generate_test_data():
    drives = VariableFrequencyDrive.generate_test_data(10)
    
    assert len(drives) == 10
    assert all(isinstance(d, VariableFrequencyDrive) for d in drives)
    models = set(d.model for d in drives)
    assert len(models) > 1 

def test_generate_test_data_with_params():
    drives = VariableFrequencyDrive.generate_test_data(
        5, 
        power=15, 
        protection_class="54",
        min_freq=0,
        max_freq=100
    )
    
    assert len(drives) == 5
    for drive in drives:
        assert drive.power == 15
        assert drive.protection_class == "54"
        assert drive.output_frequency_range == (0, 100)
def test_csv_save_load(tmp_path):
    original_drives = VariableFrequencyDrive.generate_test_data(5)
    csv_file = tmp_path / "test_drives.csv"
    
    VariableFrequencyDrive.save_to_csv(str(csv_file), original_drives)
    assert csv_file.exists()
    
    loaded_drives = VariableFrequencyDrive.load_from_csv(str(csv_file))
    assert len(loaded_drives) == 5
    assert loaded_drives[0].model == original_drives[0].model
    assert loaded_drives[0].power == original_drives[0].power
    assert loaded_drives[0].input_voltage == original_drives[0].input_voltage
    assert loaded_drives[0].protection_class == original_drives[0].protection_class
    assert loaded_drives[0].output_frequency_range == original_drives[0].output_frequency_range

def test_json_save_load(tmp_path):
    original_drives = VariableFrequencyDrive.generate_test_data(5)
    json_file = tmp_path / "test_drives.json"
    
    VariableFrequencyDrive.save_to_json(str(json_file), original_drives)
    assert json_file.exists()
    loaded_drives = VariableFrequencyDrive.load_from_json(str(json_file))
    assert len(loaded_drives) == 5
    for orig, loaded in zip(original_drives, loaded_drives):
        assert orig == loaded

def test_save_empty_list(capsys, tmp_path):
    csv_file = tmp_path / "empty.csv"
    json_file = tmp_path / "empty.json"
    
    VariableFrequencyDrive.save_to_csv(str(csv_file), [])
    captured = capsys.readouterr()
    assert "Список пуст" in captured.out
    
    VariableFrequencyDrive.save_to_json(str(json_file), [])
    captured = capsys.readouterr()
    assert "Список пуст" in captured.out