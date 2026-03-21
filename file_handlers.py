import csv
import json
import generators

def save_to_csv(filename, data_list):
    if not data_list:
        print("Список пуст, нечего сохранять")
        return
    
    dict_list = [drive.to_dict() for drive in data_list]
    fieldnames = dict_list[0].keys()
    
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(dict_list)  
    
    print(f"Данные сохранены в {filename} (CSV, {len(data_list)} записей)")

def save_to_json(filename, data_list):
    if not data_list:
        print("Список пуст, нечего сохранять")
        return
    
    json_data = [drive.to_dict() for drive in data_list]
    
    with open(filename, 'w', encoding='utf-8') as jsonfile:
        json.dump(json_data, jsonfile, ensure_ascii=False, indent=2)
    
    print(f"Данные сохранены в {filename} (JSON, {len(data_list)} записей)")

def load_from_csv(filename):
    drives = []
    
    try:
        with open(filename, 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                drive = generators.from_dict(row)
                drives.append(drive)
        
        print(f"Загружено {len(drives)} записей из {filename}")
        return drives
        
    except FileNotFoundError:
        print(f"Файл {filename} не найден")
        return []
    except Exception as e:
        print(f"Ошибка при загрузке: {e}")
        return []

def load_from_json(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as jsonfile:
            json_data = json.load(jsonfile)
        
        drives = [] 
        for i in range(len(json_data)):
            drives[i] = generators.from_dict(json_data[i])
        return drives
        
    except FileNotFoundError:
        print(f"✗ Файл {filename} не найден")
        return []
    except json.JSONDecodeError:
        print(f"Ошибка: файл {filename} не содержит корректный JSON")
        return []
    except Exception as e:
        print(f"Ошибка при загрузке: {e}")
        return []