from fd import VariableFrequencyDrive
import generators
import file_handlers

drives = generators.generate_test_data(100)
    
counter = 1
for drive in drives[:3]:
    print(f"   {counter}. {drive.info()}")
    counter += 1

file_handlers.save_to_csv("data.csv", drives)
file_handlers.save_to_json("data.json", drives)
    
loaded = file_handlers.load_from_json("data.json")
    
if loaded:
    counter = 1
    for drive in loaded[:5]:
        print(f"   {counter}. {drive.info()}")
        counter += 1
    
csv_loaded = file_handlers.load_from_csv("data.csv")
    
if csv_loaded:
    print(f"   Загружено: {len(csv_loaded)} записей")
