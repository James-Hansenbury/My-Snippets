# python 3.6

import numpy as np
from scipy.io import FortranFile
import matplotlib
matplotlib.use("TkAgg")
import pylab

initialShow = input("Would you like to plot the initial condition? Y/N ")
numSnaps = int(input("Number of snapshots to calculate: "))
if (initialShow[0] == 'N' or initialShow[0] == 'n'):
    i = 1
    numsnaps = numsnaps + 1
else:
    i = 0

while(i < numSnaps):
    # Open the Fortran unformatted binary
    iString = str(i).zfill(4)
    inFilename = "Moddat" + iString + ".bin"
    f = FortranFile(inFilename,'r')
    # Read the contents from fractal.bin in the order that they were written
    # Read nx, ny
    [nx, ny] = f.read_ints(np.int32)

    # Read wind
    wind = f.read_record('float32')
    xmin = wind[0]
    xmax = wind[1]
    ymin = wind[2]
    ymax = wind[3]

    # Read dat, then reshape into a 2D array Z for plotting (need to do transpose)
    dat = f.read_record('float32')
    Z = np.transpose(dat.reshape(nx,ny))

    # Construct the x and y vectors for plotting
    dx = (xmax - xmin)/nx
    dy = (ymax - ymin)/ny
    x = np.arange(xmin + dx/2., xmax, dx)
    y = np.arange(ymin + dy/2., ymax, dy)

    # plot
    outFilename = "Snapshot" + iString + ".png"
    pylab.pcolormesh(x,y,Z,cmap='seismic')
    pylab.xlabel('x', fontsize=16)
    pylab.ylabel('y', fontsize=16)
    pylab.colorbar()
    pylab.savefig(outFilename)
    pylab.clf()
    
    i = i+1
