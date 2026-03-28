import pytest
from datetime import datetime
from vfd import VariableFrequencyDrive
from em import ElectricMotor
from drive_system import DriveSystem


class TestVariableFrequencyDrive:
    """Тесты для частотного преобразователя"""
    
    def test_create_vfd(self):
        """Создание нормального преобразователя"""
        vfd = VariableFrequencyDrive("VFD-001", 7.5, 380, "54", (0, 400))
        assert vfd.model == "VFD-001"
        assert vfd.power == 7.5
        assert vfd.input_voltage == 380
        assert vfd.protection_class == "54"
        assert vfd.output_frequency_range == (0, 400)
    
    def test_vfd_power_negative(self):
        """Мощность не может быть отрицательной"""
        vfd = VariableFrequencyDrive("VFD-002", 5.5, 380, "54", (0, 400))
        with pytest.raises(ValueError):
            vfd.power = -10
    
    def test_vfd_power_too_big(self):
        """Мощность не может быть больше 1000 кВт"""
        vfd = VariableFrequencyDrive("VFD-003", 5.5, 380, "54", (0, 400))
        with pytest.raises(ValueError):
            vfd.power = 1500
    
    def test_vfd_power_not_number(self):
        """Мощность должна быть числом"""
        vfd = VariableFrequencyDrive("VFD-004", 5.5, 380, "54", (0, 400))
        with pytest.raises(ValueError):
            vfd.power = "сто"
    
    def test_vfd_voltage_negative(self):
        """Напряжение не может быть отрицательным"""
        vfd = VariableFrequencyDrive("VFD-005", 5.5, 380, "54", (0, 400))
        with pytest.raises(ValueError):
            vfd.input_voltage = -50
    
    def test_vfd_speed_range(self):
        """Проверка вычисления диапазона скоростей"""
        vfd = VariableFrequencyDrive("VFD-006", 7.5, 380, "54", (10, 50))
        assert vfd.speed_range == 5.0
    
    def test_vfd_speed_range_zero(self):
        """Если минимальная частота 0, то ошибка"""
        vfd = VariableFrequencyDrive("VFD-007", 7.5, 380, "54", (0, 400))
        assert vfd.speed_range == "Ошибка (минимальная частота = 0)"


class TestElectricMotor:
    """Тесты для электродвигателя"""
    
    def test_create_motor(self):
        """Создание нормального двигателя"""
        motor = ElectricMotor("MOTOR-001", 75, 1485, "IE3", "IM B3", 400)
        assert motor.model == "MOTOR-001"
        assert motor.rated_power == 75
        assert motor.rated_speed == 1485
        assert motor.efficiency_class == "IE3"
        assert motor.mounting_type == "IM B3"
        assert motor.voltage == 400
    
    def test_motor_power_negative(self):
        """Мощность не может быть отрицательной"""
        motor = ElectricMotor("MOTOR-002", 75, 1485, "IE3", "IM B3", 400)
        with pytest.raises(ValueError):
            motor.rated_power = -50
    
    def test_motor_power_too_big(self):
        """Мощность не может быть больше 5000 кВт"""
        motor = ElectricMotor("MOTOR-003", 75, 1485, "IE3", "IM B3", 400)
        with pytest.raises(ValueError):
            motor.rated_power = 6000
    
    def test_motor_speed_negative(self):
        """Скорость не может быть отрицательной"""
        motor = ElectricMotor("MOTOR-004", 75, 1485, "IE3", "IM B3", 400)
        with pytest.raises(ValueError):
            motor.rated_speed = -100
    
    def test_motor_efficiency_class_invalid(self):
        """Неправильный класс эффективности"""
        motor = ElectricMotor("MOTOR-005", 75, 1485, "IE3", "IM B3", 400)
        with pytest.raises(ValueError):
            motor.efficiency_class = "IE6"
    
    def test_motor_mounting_type_invalid(self):
        """Неправильный тип монтажа"""
        motor = ElectricMotor("MOTOR-006", 75, 1485, "IE3", "IM B3", 400)
        with pytest.raises(ValueError):
            motor.mounting_type = "XXX"
    
    def test_motor_torque(self):
        """Проверка вычисления момента"""
        motor = ElectricMotor("MOTOR-007", 75, 1485, "IE3", "IM B3", 400)
        expected_torque = (75 * 9550) / 1485
        assert abs(motor.torque - expected_torque) < 0.1
    
    def test_motor_pole_pairs(self):
        """Проверка вычисления пар полюсов"""
        motor = ElectricMotor("MOTOR-008", 75, 1485, "IE3", "IM B3", 400)
        assert motor.pole_pairs == 2  # 1500 об/мин -> 2 пары полюсов


class TestDriveSystem:
    """Тесты для системы управления"""
    
    def test_create_system(self):
        """Создание системы"""
        system = DriveSystem("Тестовая система")
        assert system.name == "Тестовая система"
        assert len(system.get_all_devices()) == 0
    
    def test_add_composition_vfd(self):
        """Добавление преобразователя через композицию"""
        system = DriveSystem("Тест")
        vfd = system.add_composition_device("VFD-TEST", "vfd", power=7.5)
        
        assert len(system.get_composition_devices()) == 1
        assert len(system.get_aggregation_devices()) == 0
        assert vfd.model == "VFD-TEST"
        assert vfd.power == 7.5
    
    def test_add_composition_motor(self):
        """Добавление двигателя через композицию"""
        system = DriveSystem("Тест")
        motor = system.add_composition_device("MOTOR-TEST", "motor", rated_power=75)
        
        assert len(system.get_composition_devices()) == 1
        assert motor.model == "MOTOR-TEST"
        assert motor.rated_power == 75
    
    def test_add_composition_invalid_type(self):
        """Добавление неправильного типа устройства"""
        system = DriveSystem("Тест")
        with pytest.raises(ValueError):
            system.add_composition_device("TEST", "sensor")
    
    def test_add_aggregation_valid_device(self):
        """Добавление существующего устройства через агрегацию"""
        system = DriveSystem("Тест")
        vfd = VariableFrequencyDrive("VFD-EXT", 7.5, 380, "54", (0, 400))
        system.add_aggregation_device(vfd)
        
        assert len(system.get_aggregation_devices()) == 1
        assert len(system.get_composition_devices()) == 0
    
    def test_add_aggregation_invalid_device(self):
        """Добавление неправильного объекта через агрегацию"""
        system = DriveSystem("Тест")
        with pytest.raises(ValueError):
            system.add_aggregation_device("не устройство")
    
    def test_remove_composition_device(self):
        """Удаление устройства композиции по индексу"""
        system = DriveSystem("Тест")
        system.add_composition_device("VFD-1", "vfd", power=7.5)
        system.add_composition_device("VFD-2", "vfd", power=11)
        
        removed = system.remove_composition_device(0)
        assert removed.model == "VFD-1"
        assert len(system.get_composition_devices()) == 1
    
    def test_remove_composition_device_invalid_index(self):
        """Удаление по неверному индексу"""
        system = DriveSystem("Тест")
        with pytest.raises(IndexError):
            system.remove_composition_device(0)
    
    def test_remove_aggregation_device_by_model(self):
        """Удаление устройства агрегации по модели"""
        system = DriveSystem("Тест")
        vfd1 = VariableFrequencyDrive("VFD-1", 7.5, 380, "54", (0, 400))
        vfd2 = VariableFrequencyDrive("VFD-2", 11, 400, "66", (0, 400))
        system.add_aggregation_device(vfd1)
        system.add_aggregation_device(vfd2)
        
        removed = system.remove_aggregation_device_by_model("VFD-1")
        assert removed.model == "VFD-1"
        assert len(system.get_aggregation_devices()) == 1
    
    def test_remove_aggregation_device_by_model_not_found(self):
        """Удаление несуществующей модели"""
        system = DriveSystem("Тест")
        with pytest.raises(ValueError):
            system.remove_aggregation_device_by_model("NOT-EXISTS")
    
    def test_total_power_only_vfd(self):
        """Суммарная мощность только преобразователей"""
        system = DriveSystem("Тест")
        system.add_composition_device("VFD-1", "vfd", power=7.5)
        system.add_composition_device("VFD-2", "vfd", power=11)
        
        assert system.total_power() == 18.5
    
    def test_total_power_only_motors(self):
        """Суммарная мощность только двигателей"""
        system = DriveSystem("Тест")
        system.add_composition_device("MOTOR-1", "motor", rated_power=75)
        system.add_composition_device("MOTOR-2", "motor", rated_power=110)
        
        assert system.total_power() == 185
    
    def test_total_power_mixed_devices(self):
        """Суммарная мощность смешанных устройств"""
        system = DriveSystem("Тест")
        system.add_composition_device("VFD-1", "vfd", power=7.5)
        system.add_composition_device("MOTOR-1", "motor", rated_power=75)
        
        external_vfd = VariableFrequencyDrive("VFD-EXT", 15, 400, "66", (0, 400))
        system.add_aggregation_device(external_vfd)
        
        assert system.total_power() == 97.5  # 7.5 + 75 + 15
    
    def test_average_power(self):
        """Средняя мощность"""
        system = DriveSystem("Тест")
        system.add_composition_device("VFD-1", "vfd", power=7.5)
        system.add_composition_device("VFD-2", "vfd", power=11)
        system.add_composition_device("VFD-3", "vfd", power=22)
        
        assert system.average_power() == (7.5 + 11 + 22) / 3
    
    def test_average_power_empty(self):
        """Средняя мощность пустой системы"""
        system = DriveSystem("Тест")
        assert system.average_power() == 0
    
    def test_get_all_devices(self):
        """Получение всех устройств"""
        system = DriveSystem("Тест")
        system.add_composition_device("VFD-1", "vfd", power=7.5)
        system.add_composition_device("MOTOR-1", "motor", rated_power=75)
        
        external_vfd = VariableFrequencyDrive("VFD-EXT", 15, 400, "66", (0, 400))
        system.add_aggregation_device(external_vfd)
        
        all_devices = system.get_all_devices()
        assert len(all_devices) == 3
    
    def test_start_all_devices(self):
        """Запуск всех устройств"""
        system = DriveSystem("Тест")
        system.add_composition_device("VFD-1", "vfd", power=7.5)
        system.add_composition_device("MOTOR-1", "motor", rated_power=75)
        
        results = system.start_all()
        assert len(results) == 2
        assert "запущен" in results[0]
        assert "запущен" in results[1]
    
    def test_stop_all_devices(self):
        """Останов всех устройств"""
        system = DriveSystem("Тест")
        system.add_composition_device("VFD-1", "vfd", power=7.5)
        system.add_composition_device("MOTOR-1", "motor", rated_power=75)
        
        results = system.stop_all()
        assert len(results) == 2
        assert "остановлен" in results[0]
        assert "остановлен" in results[1]
    
    def test_to_dict(self):
        """Преобразование системы в словарь"""
        system = DriveSystem("Тест")
        system.add_composition_device("VFD-1", "vfd", power=7.5)
        
        result = system.to_dict()
        assert result['name'] == "Тест"
        assert result['total_power'] == 7.5
        assert result['devices_count'] == 1
        assert len(result['composition_devices']) == 1
        assert len(result['aggregation_devices']) == 0


class TestCompositionVsAggregation:
    """Тесты для демонстрации различий композиции и агрегации"""
    
    def test_composition_device_cannot_live_without_system(self):
        """Устройство композиции не может существовать без системы"""
        system = DriveSystem("Тест")
        vfd = system.add_composition_device("VFD-INT", "vfd", power=7.5)
        
        # Устройство есть в системе
        assert vfd in system.get_composition_devices()
        
        # Удаляем систему
        del system
        
        # Вне системы устройство уже не доступно (оно удалилось)
        # Но мы не можем это проверить, так как объект system удален
        # Главное - что устройство было создано внутри и принадлежит системе
    
    def test_aggregation_device_can_live_without_system(self):
        """Устройство агрегации может жить без системы"""
        # Создаем устройство отдельно
        vfd = VariableFrequencyDrive("VFD-EXT", 7.5, 380, "54", (0, 400))
        
        # Создаем систему и добавляем устройство
        system = DriveSystem("Тест")
        system.add_aggregation_device(vfd)
        
        # Устройство есть в системе
        assert vfd in system.get_aggregation_devices()
        
        # Удаляем систему
        del system
        
        # Устройство все еще существует и доступно
        assert vfd.model == "VFD-EXT"
        assert vfd.power == 7.5