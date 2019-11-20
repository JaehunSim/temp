import math
import seaborn as sns
from matplotlib import pyplot as plt
import numpy as np

def f(x, e=0.1):
    if -1*e <= x <= e:
        return 1
    if 2*e <= abs(x):
        return 0
    result = math.exp(-1*(abs(x)-e)**2 / (4*e**2 - x**2))
    return result

def f1(x, e=0.1):
    d = 0.00000001
    return (f(x) - f(x-d)) / d

def f2(x, e=0.1):
    d = 0.00000001
    return (f1(x) - f1(x-d)) / d

x = np.arange(-0.3, 0.30001, 0.00005)
x = x.tolist()

f(0.15)
f1(0.15)
f2(0.15)


y1 = []
for x_coord in x:
    y1.append(f1(x_coord))
plt.figure(figsize=(16, 10))
sns.scatterplot(x, y1)
plt.grid()
plt.show()

y2 = []
for x_coord in x:
    y2.append(f2(x_coord))
plt.figure(figsize=(16, 10))
sns.scatterplot(x, y2)
plt.grid()
plt.show()