from vfd import VariableFrequencyDrive
from em import ElectricMotor

class DriveSystem:
    def __init__(self, name):
        self.name = name
        self._composition_devices = []
        self._aggregation_devices = []
    
    def add_composition_device(self, model, device_type, **params):
        if device_type == "vfd":
            device = VariableFrequencyDrive(
                model=model,
                power=params.get('power', 0),
                input_voltage=params.get('input_voltage', 380),
                protection_class=params.get('protection_class', '20'),
                frequency_range=params.get('frequency_range', (0, 50))
            )
        elif device_type == "motor":
            device = ElectricMotor(
                model=model,
                rated_power=params.get('rated_power', 0),
                rated_speed=params.get('rated_speed', 1500),
                efficiency_class=params.get('efficiency_class', 'IE3'),
                mounting_type=params.get('mounting_type', 'IM B3'),
                voltage=params.get('voltage', 400)
            )
        else:
            raise ValueError(f"Неизвестный тип устройства: {device_type}")
        
        self._composition_devices.append(device)
        return device
    
    def add_aggregation_device(self, device):
        if not isinstance(device, (VariableFrequencyDrive, ElectricMotor)):
            raise ValueError("Устройство должно быть экземпляром VariableFrequencyDrive или ElectricMotor")
        self._aggregation_devices.append(device)
        return device
    
    def remove_composition_device(self, index):
        if 0 <= index < len(self._composition_devices):
            return self._composition_devices.pop(index)
        raise IndexError("Индекс вне диапазона")
    
    def remove_aggregation_device(self, index):
        if 0 <= index < len(self._aggregation_devices):
            return self._aggregation_devices.pop(index)
        raise IndexError("Индекс вне диапазона")
    
    def remove_aggregation_device_by_model(self, model):
        for i, device in enumerate(self._aggregation_devices):
            if device.model == model:
                return self._aggregation_devices.pop(i)
        raise ValueError(f"Устройство с моделью {model} не найдено")
    
    def get_all_devices(self):
        return self._composition_devices + self._aggregation_devices
    
    def get_composition_devices(self):
        return self._composition_devices.copy()
    
    def get_aggregation_devices(self):
        return self._aggregation_devices.copy()
    
    def start_all(self):
        results = []
        for device in self.get_all_devices():
            if hasattr(device, 'start'):
                results.append(device.start())
            else:
                results.append(f"{device.model}: метод start не реализован")
        return results
    
    def stop_all(self):
        results = []
        for device in self.get_all_devices():
            if hasattr(device, 'stop'):
                results.append(device.stop())
            else:
                results.append(f"{device.model}: метод stop не реализован")
        return results
    
    def show_all_info(self):
        info_list = []
        info_list.append(f"\n=== Drive System: {self.name} ===")
        info_list.append("\n--- Композиция (созданы внутри системы) ---")
        for i, device in enumerate(self._composition_devices):
            info_list.append(f"{i}: {device.info()}")
        
        info_list.append("\n--- Агрегация (добавлены извне) ---")
        for i, device in enumerate(self._aggregation_devices):
            info_list.append(f"{i}: {device.info()}")
        
        return "\n".join(info_list)
    
    def total_power(self):
        total = 0
        for device in self.get_all_devices():
            if isinstance(device, VariableFrequencyDrive):
                total += device.power
            elif isinstance(device, ElectricMotor):
                total += device.rated_power
        return total
    
    def average_power(self):
        devices = self.get_all_devices()
        if not devices:
            return 0
        return self.total_power() / len(devices)
    
    def to_dict(self):
        return {
            'name': self.name,
            'composition_devices': [device.to_dict() for device in self._composition_devices],
            'aggregation_devices': [device.to_dict() for device in self._aggregation_devices],
            'total_power': self.total_power(),
            'devices_count': len(self.get_all_devices())
        }