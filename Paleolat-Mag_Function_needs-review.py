#! /usr/bin/env python

# Author: James Hansenbury
# Creation: 9/29/2021

import numpy as np
import matplotlib.pyplot as plt
d2r = np.pi/180
r2d = 180/np.pi

def inc_to_lat(inclination=[], error=None):
	'''
	This function calculates latitude from a set of inclinations, with error optionality.
	INPUTS------------------------------------------------
	inclination = list of inclinations to calculate (in degrees)
	error = optional, the error in inclination.
		Can be an integer or 1-D list of errors corresponding to each inclination
	OUTPUTS-----------------------------------------------
	latitude = list of latitudes corresponding to input inclination
	laterr = list of upper and lower errors corresponding to each latitude
		*Will not output if no error input
	'''
	latitude = r2d*np.arctan(.5*np.tan(d2r*inclination))
	if error:
		inclinmax = inclination + error
		inclinmin = inclination - error
		hierr = r2d*np.arctan(.5*np.tan(d2r*inclinmax)) - latitude
		loerr = latitude - r2d*np.arctan(.5*np.tan(d2r*inclinmin))
		laterr = [loerr, hierr]
		return latitude, laterr
	else:
		return latitude

#Declare variables for problem #14 of CH. 10 
incs = [-54, -56, -55, -50, -38, 0, 10 , 43]
ierr = 2
time = [300, 250, 190, 160, 140, 80, 60, 0]
terr = 4

#use function and plot data
incs = np.array(incs)
time = np.array(time)
lats,laterr = inc_to_lat(incs, ierr)
#print(lats)

plt.errorbar(time, lats, xerr=terr, yerr=laterr, ecolor='r', capsize=3., barsabove=True)
plt.gca().invert_xaxis()
pltitle = "Latitude Of Block Over Time by Paleomagnetism"
plt.title(pltitle)
#plt.legend(legstr)
plt.xlabel("Age in Ma")
plt.ylabel("Latitude")
plt.grid()
plt.show()