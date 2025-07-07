# words = ["Там", "стоит", "стол"]
# selected = ["стоит"]

# remaining = [w for w in words if w not in selected]
# # результат: ["Там", "стол"]
# print(remaining)

# import random

# mood = random.random()

# print(mood)

# print(1/8)

# print(1/4)

# print (5/8)

import threading

def print_numbers():
    for i in range(10):
        print(i)

# print_numbers()

thread = threading.Thread(target=print_numbers)

thread.start()