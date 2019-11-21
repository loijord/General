import numpy as np
import matplotlib.pyplot as plt

skaiciai = np.linspace(0,2,100)
for i in range(3): skaiciai = np.sqrt(skaiciai)
plt.plot(np.linspace(0,10,100), skaiciai)
plt.show()