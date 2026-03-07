from vfd import VariableFrequencyDrive

vfd1 = VariableFrequencyDrive("VFD-007", 7.5, 380, "54", (200, 400))
vfd2 = VariableFrequencyDrive("Altivar 320", 15.0, 480, "21", (200, 500))

print(vfd1)
print(vfd1 == vfd2)
print(vfd1 + vfd2)

vfd3 = eval(vfd2.__repr__())
print(vfd3)
print(vfd2)

print(vfd3.__repr__())
print(vfd2.__repr__())

if vfd2 == vfd3:
    print("Same obj")

print("____________Лаба_5______________")

test_drives = VariableFrequencyDrive.generate_test_data(5)
for i, drive in enumerate(test_drives, 1):
    print(f"{i}. {drive.info()}")
    print(f"{i}.{drive.to_dict()}")

motorchiki = VariableFrequencyDrive.generate_test_data(100)
VariableFrequencyDrive.save_to_csv("data.csv", motorchiki)
VariableFrequencyDrive.save_to_json("data.json", motorchiki)

loaded = VariableFrequencyDrive.load_from_json("data.json")
for i, drive in enumerate(loaded[:100], 1):
    print(f"{i}.{drive.info}")
