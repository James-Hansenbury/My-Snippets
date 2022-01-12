#! /usr/bin/env python

import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import pylab

def PLOTXY(x,y,title,info):
    done = 0
    x.sort()
    y.sort()
    xLen = len(x)-1
    yLen = len(y)-1
    xBoundLo = x[0] - (x[xLen]-x[0])/15
    xBoundHi = x[xLen] + (x[xLen]-x[0])/15
    yBoundLo = y[0] - (y[yLen]-y[0])/15
    yBoundHi = y[yLen] + (y[yLen]-y[0])/15
    plt.plot(x, y, 'bo-')
    plt.axis([xBoundLo,xBoundHi,yBoundLo,yBoundHi])
    plt.ylabel('Time')
    plt.xlabel('Distance')
    plt.title(title)
    plt.savefig('TDgraph(%s).png'%info)
    plt.show()
    done = 1
    return done

#P.S. See Data-Process_subrout_input.f90 in fortran folder for formatting program
print("This program will graph data from a file formatted by F15Lab6.F90")
all = False
iter = 0
line = str()
inFileN = input('Input file name:')
with  open(inFileN) as inFile:
    for line in inFile:
        if (line[1] != ' '):
            if (iter != 0):
                PLOTXY(distance, time, title, event[0])
                if (all == False):
                    answer = input("Continue graphing calculations? Y/N\nType A or All to compute all graphs.\n")
                    if (answer[0] == 'n' or answer[0] == 'N'):
                        print("Goodbye!")
                        break
                    elif (answer[0] == 'a' or answer[0] == 'A'):
                        all = True
            event = line.split()
            print(event[0])
            title = 'Earthquake ID %d, Magnitude %g, Depth %g km'%(int(event[0]), float(event[5]), float(event[7]))
            iter = 0
            time = list()
            distance = list()
        else:
            station = line.split()
            distance.append(float(station[0]))
            time.append(float(station[1]))
            iter += 1
print("No more data to graph!")