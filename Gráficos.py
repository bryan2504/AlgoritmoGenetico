import matplotlib.pyplot as plt
from matplotlib import style 
import numpy as np

x1 = [1,2,4,8,15,20,25,30,35,40]
x2 = [0.36,2.72,7.69,27.84,65.69,83.76,92.70,94.25,96.50,96.99]

y1 = [1,2,4,8,15,20,25,30,35,40]
y2 = [0.37,2.75,8.83,29.84,68.79,84.75,93.70,95.25,97.50,98.01]

z1 = [1,2,4,8,15,20,25,30,35,40]
z2 = [0.37,2.82,9.91,31.05,70.94,89.08,97.64,98.76,99.52,99.93]

plt.plot(x1,x2)
plt.plot(y1,y2)
plt.plot(z1,z2)
plt.title('Comparaciones')
plt.ylabel('% de similitud')
plt.xlabel('# de generaciones')
plt.show()
