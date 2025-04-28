import matplotlib.pyplot as plt

x = [1,2,3,4,5]
y = [2,4,6,8,10]

plt.plot(x, y, label='Line 1', marker='')

plt.scatter(x, y, color = 'red', label = 'Scatter Points')

x2 = [1, 2, 3, 4, 5]
y2 = [3, 5, 7, 9, 11]
plt.plot(x2, y2, label='Line 2', linestyle='--')  
