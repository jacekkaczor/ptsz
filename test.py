import math
import time as times
import numpy as np
import random




a  = np.arange(10)

b = []
for i in range(10):
    b.append(i)


print(a,b)

for i in range(10):
    print(np.random.choice(a,1,a))