import numpy as np
import array as arr

ele = arr.array('i',[1,2,3])
for i in ele:
    print(f"{i}", end=",")

data = np.array([1,2,3,4])
for i in data:
    print(f"{i}", end=",")

data = [10, 5, 20, 8]

for i in data:
    if i>i+1:
        print(f"largest number{i}")

