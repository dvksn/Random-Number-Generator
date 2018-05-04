import numpy as np
import scipy.stats as stats
import pylab as pl
import math



text_file = open("randomNumbersNew.txt")

data = text_file.read().split('\n')
del data[-1]
data = [float(x) for x in data]
print(len(data))


# histogram plot 
print (len(data))
pl.hist(data[:10000],normed=True)
pl.xlabel("random numbers")
pl.show()


# normal plot 
print (len(data))
pl.plot(data[0:10000])
pl.xlabel("random numbers")
# pl.hist(data,normed=True) 
pl.show()


lam = 0.5

newdata = []
for x in data:
    temp = (-1.0/lam)*(math.log(1-x))
    newdata.append(temp)


print (len(newdata))
pl.plot(newdata[0:1000])
pl.xlabel("random numbers")
# pl.hist(data,normed=True) 
pl.show()


pl.hist(newdata[:1000],normed=True)
pl.xlabel("random numbers")
pl.show()



