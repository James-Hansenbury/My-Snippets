#! /usr/bin/env python

# Author: James Hansenbury
# Creation: 9/29/2021

import numpy as np
import matplotlib.pyplot as plt

def filter_pt(xin=[],indata=[],points=3):
	'''
	This function applies a filter to a set of data to smooth its curve.
	INPUTS------------------------------------------------
	xin - The position of measurements taken along an axis
	indata - The measurements made at each position
	points - Number of points used to smooth data
	*xin and indata must have the same lengths
	*Length of indata must be larger than points
	OUTPUTS-----------------------------------------------
	outx - shortened x-value list corresponding to new dataset
	outdata - smoothed data
	'''
	points = int(points)
	datalength = len(indata)
	if datalength != len(xin):
		print("Number of positions must match number of measurements.")
		return [], []
	if datalength <= points:
		print("Data input must have more points than the filter is reducing by.")
		return [], []
	newlength = datalength-points+1
	
	outdata = np.zeros(newlength)
	outx = np.zeros(newlength)
	for i in np.arange(newlength):
		outdata[i] = np.mean(indata[i:i+points])
		if points%2 == 0:
			outx[i] = np.mean([x[int(i+points/2-1):int(i+3*points/2)]])
		else:
			outx[i] = x[int(i+(points-1)/2)]
	return outx, outdata

#utilize the smoothing function and plot data
x = np.arange(19)
rawdata = [-3,2,1,4,0,4,-1,3,0,1,-4,0,-4,-1,-4,1,0,2,4]
pts = [4,3,5]
legstr= ["Raw Measurement Data"]

print("Maximum and minimum values for raw data:\n{:.3f}, {:.3f}".format(max(rawdata),min(rawdata)))
plt.plot(x, rawdata, 'co-')
for i in pts:
	xfilt, datafilt = filter_pt(x, rawdata, i)
	plt.plot(xfilt, datafilt)
	legstr.append("{}-point Filter".format(i))
	print("Maximum and minimum values for {}-point Filter:\n{:.3f}, {:.3f}".format(i,max(datafilt),min(datafilt)))

pltitle = "Measured Data With Discrete Filters Overlaid"
plt.title(pltitle)
plt.legend(legstr)
plt.xlabel("Distance in m")
plt.ylabel("Amplitude")
plt.grid()
plt.show()