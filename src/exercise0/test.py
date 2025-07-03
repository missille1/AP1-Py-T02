words = ["Там", "стоит", "стол"]
selected = ["стоит"]

remaining = [w for w in words if w not in selected]
# результат: ["Там", "стол"]
print(remaining)