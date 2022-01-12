#! /usr/bin/env python3.6
#UCSB ES 232 Python assignment 2
#James Danbury

import numpy as np

print("This program will calculate any real roots of a quadratic equation.")
a = float()
b = float()
c = float()
while (True):
    try:
        a = float(input("Input the three coefficients a, b, and c for the following quadratic equation:\naX^2+bX+c\nInput all 0's to exit.\na= "))
        b = float(input("b= "))
        c = float(input("c= "))
    except ValueError:
        print("Incorrect type of input, coefficients must be numerical.")
    if (a == 0 and b == 0 and c == 0):
        break
    w = b**2-4*a*c
    if (w > 0):
        numRoots = 2
        print("There are two real roots.")
        rootFirst = (-b+np.sqrt(w))/(2*a)
        rootSecond = (-b-np.sqrt(w))/(2*a)
        print("The roots are: {0:g}, {1:g}".format(rootFirst, rootSecond))
    elif (w < 0):
        numRoots = 0
        print("There are no real roots.")
    else:
        numRoots = 1
        print("There is one real root.")
        root = -b/(2*a)
        print("The root is: {0:g}".format(root))
print("Goodbye!")