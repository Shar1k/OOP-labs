from drive_system import DriveSystem
from vfd import VariableFrequencyDrive
from em import ElectricMotor

if __name__ == "__main__":
    system = DriveSystem("Производственная линия №1")
    
    print("=== Композиция: создание устройств внутри системы ===")
    vfd1 = system.add_composition_device("VFD-001", "vfd", 
                                         power=7.5, 
                                         input_voltage=380,
                                         protection_class="54",
                                         frequency_range=(0, 400))
    
    motor1 = system.add_composition_device("MOTOR-001", "motor",
                                           rated_power=7.5,
                                           rated_speed=1450,
                                           efficiency_class="IE3",
                                           mounting_type="IM B3",
                                           voltage=380)
    
    print("Созданы устройства внутри системы")
    
    print("\n=== Агрегация: добавление внешних устройств ===")
    external_vfd = VariableFrequencyDrive("VFD-EXTERNAL", 15, 400, "66", (0, 400))
    external_motor = ElectricMotor("MOTOR-EXTERNAL", 22, 1480, "IE4", "IM B5", 400)
    
    system.add_aggregation_device(external_vfd)
    system.add_aggregation_device(external_motor)
    print("Добавлены внешние устройства")
    
    print(system.show_all_info())
    
    print("\n=== Запуск всех устройств ===")
    for result in system.start_all():
        print(f"  {result}")
    
    print("\n=== Останов всех устройств ===")
    for result in system.stop_all():
        print(f"  {result}")
    
    print(f"\n=== Агрегированные характеристики ===")
    print(f"Суммарная мощность: {system.total_power()} кВт")
    print(f"Средняя мощность: {system.average_power():.2f} кВт")
    
    print("\n=== Удаление устройства по модели (агрегация) ===")
    system.remove_aggregation_device_by_model("VFD-EXTERNAL")
    print("Удален VFD-EXTERNAL")
    
    print("\n=== Удаление устройства по индексу (композиция) ===")
    removed = system.remove_composition_device(0)
    print(f"Удален: {removed}")
    
    print(system.show_all_info())
    
    print("\n=== Словарь с данными системы ===")
    import json
    print(json.dumps(system.to_dict(), ensure_ascii=False, indent=2, default=str))
    
    print("\n=== Демонстрация различий композиции и агрегации ===")
    system2 = DriveSystem("Тестовая система")
    
    print("Композиция: устройство создается внутри системы")
    internal_device = system2.add_composition_device("INTERNAL", "vfd", power=5.5, input_voltage=380)
    print(f"  Создано: {internal_device}")
    
    print("Агрегация: устройство создается снаружи и затем добавляется")
    external_device = VariableFrequencyDrive("EXTERNAL", 11, 400, "54", (0, 400))
    system2.add_aggregation_device(external_device)
    print(f"  Создано снаружи: {external_device}")
    
    print("\nПри удалении system2:")
    print("  - Композиционные устройства будут уничтожены вместе с system2")
    print("  - Агрегированные устройства продолжат существовать")
    del system2
    print("  system2 удалена")
    print(f"  Внешнее устройство все еще существует: {external_device}")