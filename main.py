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

