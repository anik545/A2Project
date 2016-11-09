from functools import partial

import time
import numpy
import scipy.optimize
import matplotlib.pyplot as pp
from sympy import arg,I
from math import atan2,sqrt,pi,atan
from cmath import phase


def z(x, y):
    n=x+y*1j
    
    return 2*atan((y**2 + (x + 4)**2)*(sqrt(16*y**2/(y**2 + (x + 4)**2)**2 + (x*(x + 4) + y**2)**2/(y**2 + (x + 4)**2)**2) - (x*(x + 4) + y**2)/(y**2 + (x + 4)**2))/(4*y)) - pi/4
    #return atan2(y-2,x-2)+pi/4

x_window = -10, 10
y_window = -10, 10

xs = []
ys = []
t1=time.time()
last=1
for x in numpy.linspace(*x_window, num=200):
    try:
        # A more efficient technique would use the last-found-y-value as a
        # starting point
        y = scipy.optimize.fsolve(partial(z, x), last)
        last=y
    except ValueError:
        # Should we not be able to find a solution in this window.
        pass
    else:
        xs.append(x)
        ys.append(y)
t2=time.time()
print(t2-t1,'s')
pp.plot(xs, ys)
pp.xlim(*x_window)
pp.ylim(*y_window)
pp.show()
