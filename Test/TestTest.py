import numpy as np
import matplotlib.pyplot as plt

x = [1,2,3,4,5,6]
y = [3,5,7,10,9,3]

fit = np.polyfit(x,y,1)
fit_fn = np.poly1d(fit)

plt.plot(x,y, 'yo', x, fit_fn(x), '--k')
plt.xlim(0, 10)
plt.ylim(0, 15)
plt.show()

