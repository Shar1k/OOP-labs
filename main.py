from vfd import VariableFrequencyDrive
import generators
import file_handlers

drives = generators.generate_test_data(100)

def print_all_sensors(sensors):
    for sensor in sensor:
        print(f"{sensor.read_value} {sensor.unit}")