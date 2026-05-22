import numpy as np

data = np.array([1,2,3,4])
for i in data:
    print(f"{i}", end=",")

data = [10, 5, 20, 8]

for i in data:
    if i>i+1:
        i++
        print(f"largest number{i}")

