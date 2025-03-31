import numpy as np
#cREATE List of tuples
data = [
    (10, 14629),
    (20, 25600),
    (30, 37002),
    (40, 50000),
    (50, 63179),
    (60, 79542),
    (70, 100162),
    (80, 130000),
    (90, 184292)
    ]

#convert list to a numpy array
arr=np.array(data)

print("Dimensions of the array: ", arr.shape)
print("  Number of elements in the array: ", arr.size)

print("\n Table of Percantiles and Household Income: ")
print("Percantile\tHousehold Income")
for row in arr:
    print(f"{row[0]}\t\t{row[1]}")