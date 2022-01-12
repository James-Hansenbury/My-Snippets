#! /home/James/ES232
# python 3.6

#This program reads a fortran formatted file and plots it.
#Intended for use with fractal data

import numpy as np
from scipy.io import FortranFile
import matplotlib
matplotlib.use("TkAgg")
import pylab

# Open the Fortran unformatted binary
infilen = "fractal.bin"
f = FortranFile(infilen,'r')
# Read the contents from fractal.bin in the order that they were written
# Read nx, ny
[nx, ny] = f.read_ints(np.int32)
print('nx, ny =', nx, ny)

# Read wind
wind = f.read_record('float32')
xmin = wind[0]
xmax = wind[1]
ymin = wind[2]
ymax = wind[3]
print('xmin, xmax, ymin, ymax =', xmin, xmax, ymin, ymax)

# Read dat, then reshape into a 2D array Z for plotting (need to do transpose)
dat = f.read_record('float32')
Z = np.transpose(dat.reshape(nx,ny))

# Construct the x and y vectors for plotting
dx = (xmax - xmin)/nx
dy = (ymax - ymin)/ny
x = np.arange(xmin + dx/2., xmax, dx)
y = np.arange(ymin + dy/2., ymax, dy)

# plot
pylab.pcolormesh(x,y,np.log10(Z),cmap='jet')
pylab.xlabel('x', fontsize=16)
pylab.ylabel('y', fontsize=16)
pylab.colorbar()
pylab.show()