#! /usr/bin/env python

# Author: James Hansenbury
# Creation: 11/22/21

#Uses a working folder instead of the default appdata folder
#----------Comment this section for use on other computers----------
import os
dir_name = r"C:\Users\james\OneDrive\Documents\Utility\Python_Output"
try:
	os.chdir(dir_name)
except OSError:
	print("Could not change directory, exiting.")
	exit
print("Working Directory:\n{}".format(os.getcwd()))
#--------------------------------------------------------------------
#Start main program section

import numpy as np
from matplotlib import cm
import matplotlib.pyplot as plt

#Grab data from files
#Note the columns: 0=time | 1=mag data | 2=x dist | 3=y dist
filename_meas = "Lab2_MagData.txt"
filename_norm = "Lab2_MagNorm.txt"

measurements = np.loadtxt(filename_meas)
normalizations = np.loadtxt(filename_norm)

#Calculate and plot diurnal variations
#Note: I used a N=1 fit since diurnal variations are smooth and gradual enough that more complex 
#equations aren't needed for 1 hour of observations. Furthermore, the natural variation in measurements 
#had greater magnitude than the diurnal variation, so a linear plot will help to reduce this noise.
n = 1
normalizations[:,1] -= min(normalizations[:,1])
norm_eq = np.polyfit(normalizations[:,0], normalizations[:,1], n)
tvals = np.arange(int(min(normalizations[:,0]-1)),int(max(normalizations[:,0]+2)))
#Plot the diurnal variations
plot_title = "Diurnal Variation Plot With Linear Fit"
plt.plot(normalizations[:,0], normalizations[:,1], 'rx')
plt.plot(tvals,np.polyval(norm_eq,tvals),'b-')
plt.title(plot_title)
plt.xlabel("Time (min)")
plt.ylabel("Magnitude (nT)")
plt.grid('on')
plt.show()

#-----------------------------------
#Apply diurnal variation to dataset
measurements[:,1] -= np.polyval(norm_eq,measurements[:,0])

#Now we average the normalized measurements for each point
#This is done by finding each unique location and averaging all measurements (including time) for this point
meas_unique = np.unique(measurements[:,2:],axis=0)
avg = np.empty((len(meas_unique),4))
j = 0
for i in meas_unique:
	booleangrid = (i==measurements[:,2:])
	boolean = np.array(booleangrid[:,0]*booleangrid[:,1])
	time = np.average(np.trim_zeros(boolean*measurements[:,0]))
	avgmeas = np.average(np.trim_zeros(boolean*measurements[:,1]))
	x = i[0]
	y = i[1]
	location = np.array([time, avgmeas, x, y])
	avg[j,:] = [time, avgmeas, x, y]
	j += 1
#Convert averages into usable form by eliminating repeat values
xcoords = np.unique(avg[:,2], axis=0)
ycoords = np.unique(avg[:,3], axis=0)
xlength = len(xcoords)
ylength = len(ycoords)
zplot = np.empty((xlength,ylength))
# i = 0
# for xit in xcoords:
# 	j = 0
# 	for yit in ycoords:
# 		index = int(xlength*i+j)
# 		zplot[i,j] = avg[index,1]
# 		j += 1
# 	i += 1

i = 0
for j in np.arange(0,xlength):
	zplot[j,:] = avg[i*ylength:(i+1)*ylength,1]
	i += 1

#Next, we'll plot the surface
xplot, yplot = np.meshgrid(xcoords,ycoords)
fig, ax = plt.subplots(subplot_kw={"projection":"3d"})
surf = ax.plot_surface(xplot, yplot, zplot, cmap=cm.coolwarm)
plot_title = "Surface of Magnetic Readings"
fig.colorbar(surf, shrink=.75)
ax.set_title(plot_title)
ax.set_xlabel("Distance E (m)")
ax.set_ylabel("Distance N (m)")
ax.set_zlabel("Magnetic Strength (nT)")
plt.show()


#----------------------------------------------------
#Next we find the max and min values for the transect:

ind_min = np.where(zplot == np.amin(zplot))
ind_max = np.where(zplot == np.amax(zplot))
x_min = float(xcoords[ind_min[0]])
y_min = float(ycoords[ind_min[1]])
x_max = float(xcoords[ind_max[0]])
y_max = float(ycoords[ind_max[1]])

#Here we generate the x-y trace of the transect
if x_min == x_max:
	sectx = [0,x_min]
	secty = 0
	bearing = 90
elif y_min == y_max:
	sectx = 0
	secty = [0,y_min]
	bearing = 0
else:
	secty = np.polyfit([x_min, x_max], [y_min, y_max], 1)
	sectx = [1/secty[0],-secty[1]/secty[0]]
	bearing = round(np.arctan(np.polyval(secty,5)/5)*180/np.pi, 3)
secty,sectx = [np.array(secty),np.array(sectx)]

#Now we find the z-values at every intersection of the transect with the surface mesh lines
#This has to be done for both the x mesh lines and the y mesh lines for full accuracy on diagonals
x_ints = np.zeros([xlength,3])
j = 0
for xit in xcoords:
	if not secty.any():
		break
	y = round(xit*secty[0]+secty[1], 6)
	if y > ycoords.max() or y < ycoords.min():
		continue
	x_ind, = np.where(xcoords == xit)
	y_ind, = np.where(ycoords == round(y,6))
	if y_ind.size:
		z = float(zplot[x_ind,y_ind])
	else:
		ylo = max(ycoords[np.where(ycoords < y)])
		yhi = min(ycoords[np.where(ycoords > y)])
		zlo = zplot[x_ind,np.where(ycoords == ylo)]
		zhi = zplot[x_ind,np.where(ycoords == yhi)]
		line_yz = np.polyfit([ylo,yhi],np.append(zlo,zhi), 1)
		z = np.polyval(line_yz, y)
	x_ints[j,:] = [xit, y, z]
	j += 1

y_ints = np.zeros([ylength,3])
j = 0
for yit in ycoords:
	if not sectx.any():
		break
	x = round(yit*sectx[0]+sectx[1], 6)
	if x > xcoords.max() or x < xcoords.min():
		continue
	y_ind, = np.where(ycoords == yit)
	x_ind, = np.where(xcoords == x)
	if x_ind.size:
		z = float(zplot[x_ind,y_ind])
	else:
		xlo = max(xcoords[np.where(xcoords < x)])
		xhi = min(xcoords[np.where(xcoords > x)])
		zlo = zplot[np.where(xcoords == xhi),y_ind]
		zhi = zplot[np.where(xcoords == xhi),y_ind]
		line_xz = np.polyfit([xlo,xhi], np.append(zlo,zhi), 1)
		z = np.polyval(line_xz, x)
	y_ints[j,:] = [x, yit, z]
	j += 1
#Now we combine the two sets of data, sort it, and remove the zeros
intercepts = np.append(x_ints,y_ints,axis=0)
intercepts = intercepts[np.any(intercepts != 0, axis=1)]
intercepts = np.unique(intercepts, axis=0)
if x_min == x_max:
	intercepts = intercepts[np.argsort(intercepts[:, 1])]
else:
	intercepts = intercepts[np.argsort(intercepts[:, 0])]

#Next we find the distance along the transect
distance = np.zeros(intercepts.shape[0])
slope = np.zeros(intercepts.shape[0]-1)
steepest = 0
for i in np.arange(1,len(distance)):
	dist_minor = np.sqrt((intercepts[i,0]-intercepts[i-1,0])**2+(intercepts[i,1]-intercepts[i-1,1])**2)
	print(dist_minor)
	distance[i] = distance[i-1]+dist_minor
	slope[i-1] = (intercepts[i,2]-intercepts[i-1,2])/dist_minor

#Here we calculate the result of Peter's half-slope method to find an estimated depth of anomaly
#Since slope is calculated between points, we assume the point is on the inside edge
if np.argmin(intercepts[:,2]) > np.argmax(intercepts[:,2]):
	slope = -slope
	print(slope)
steep_index = np.argmax(np.abs(slope))
steepest = slope[steep_index]
half_steep = steepest/2

try:
	slopelo = min(slope[np.where(slope[:steep_index] <= half_steep)])
except ValueError:
	slopelo_ind = 0
else:
	slopelo_ind, = np.where(slope == slopelo)
	slopelo_ind += 1
try:
	slopehi = max(slope[np.where(slope[steep_index:] <= half_steep)])
except ValueError:
	slopehi_ind = -1
else:
	slopehi_ind, = np.where(slope == slopehi)
	slopehi_ind += 1

depth = float(1.6*(distance[slopehi_ind]-distance[slopelo_ind]))
print(depth)

#Plot the transect
plot_title = "Transect Through Max/Min of Measurements"
plt.plot(distance,intercepts[:,2])
plt.title(plot_title)
plt.xlabel("Distance (m) Across Transect Bearing {} Degrees".format(bearing))
plt.ylabel("Magnetic Strength (nT)")
plt.grid('on')
plt.show()