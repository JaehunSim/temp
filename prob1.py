import math
import seaborn as sns
from matplotlib import pyplot as plt
import numpy as np
from scipy import misc

def f(x, e=0.1):
    if -1*e <= x <= e:
        return 1
    if 2*e <= abs(x):
        return 0
    result = math.exp(-1*(abs(x)-e)**2 / (4*e**2 - x**2))
    return result

x = np.arange(-0.3, 0.30001, 0.00005)
x = x.tolist()

y2 = []
for x_coord in x:
    y2.append(misc.derivative(f, x_coord, dx=1e-8))
plt.figure(figsize=(16, 10))
sns.scatterplot(x, y2)
plt.grid()
plt.show()
