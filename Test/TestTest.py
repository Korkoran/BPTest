import numpy as np
import matplotlib.pyplot as plt

x = [1,2,3,4,5,6]
y = [3,5,7,10,9,3]

fit = np.polyfit(x,y,1)
fit_fn = np.poly1d(fit)

#plt.plot(x,y, 'yo', x, fit_fn(x), '--k')
#plt.xlim(0, 10)
#plt.ylim(0, 15)
#plt.show()

data = [5,6,6,8,9,3,6,5,7,4,10,15,6,11,5,6,2,3,4,8]

print np.mean(data)
data.sort()
print data

print data[len(data)/4:len(data)-(len(data)/4)]
print len(data)
center = np.mean(data)
spread = min(data)
flier_high = data[len(data)/4]
flier_low = data[len(data)-(len(data)/4)]


plt.boxplot([1,2,3,4,5,6,5,5,5,5,5,5,5,5,6,6,6,6,6,7,8,9], showfliers=True)
plt.show()

