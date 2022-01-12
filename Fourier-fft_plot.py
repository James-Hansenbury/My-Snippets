#Earth Science 131
#UCSB Winter 2019, Professor Matoza
#Lab 2: Discrete Fourier Transforms
#James Danbury

import numpy as np
from scipy import fftpack as fftP
import matplotlib.pyplot as plt
from matplotlib import rcParams

#Question 1 -------------------------------------------
freqFunc = 1
count = 1

fig = plt.figure(1,[10,10])
while(freqFunc <= 9):
    freqSample = 20. #Hertz
    tMax = 51.2 #seconds
    dt = 1 / freqSample
    t = np.arange(0, tMax+dt, dt)

    if(len(t)%2 != 0):
        t = t[0:-1]
    mid = int(len(t)/2)
    y = np.sin(2*np.pi*freqFunc*t)

    FyRaw = fftP.fft(y)
    FyNorm = abs(FyRaw/len(t))
    Fy = FyNorm[0:mid+1]
    freqVec = freqSample*np.arange(0,mid+1)/len(Fy)

    subTitle = "f = " + str(freqFunc)
    plt.subplot(3, 3, count)
    plt.plot(freqVec, Fy, 'k', linewidth = 1.4)
    plt.title(subTitle)
    plt.xlabel('f [Hz]', fontsize=8)
    plt.ylabel('|A(f)|', fontsize=8)
    count = count+1
    freqFunc = freqFunc+1
plt.show()

#Question 2 -------------------------------------------

freq1 = 5
freq2 = 10
freq3 = 12
amp1 = .7
amp2 = .25
amp3 = .9

freqSample = 100. #Hertz
tMax = 200 #seconds
dt = 1 / freqSample
tSmall = np.arange(0, 5+dt, dt)

#a)
ySmall = amp1*np.sin(2*np.pi*freq1*tSmall)+amp2*np.sin(2*np.pi*freq2*tSmall)+amp3*np.sin(2*np.pi*freq3*tSmall)

fig = plt.figure()
plt.plot(tSmall, ySmall, 'k', linewidth = 1.4)
plt.title("3-part Signal")
plt.xlabel('t [s]', fontsize=18)
plt.ylabel('A', fontsize=18)
plt.show()

#b)
t = np.arange(0, tMax+dt, dt)
if(len(t)%2 != 0):  #make even number of values
    t = t[0:-1]
mid = int(len(t)/2) #half the number of values
y = amp1*np.sin(2*np.pi*freq1*t)+amp2*np.sin(2*np.pi*freq2*t)+amp3*np.sin(2*np.pi*freq3*t) #Solve for y with even t

FyRaw = fftP.fftshift(fftP.fft(y)) #transform and center y
FyNorm = abs(FyRaw/len(t))  #Normalize function
Fy = 2*FyNorm[:len(t)]  #Multiply by two for correct amplitude two sided

n = np.arange(-mid,mid) #Number of values for domain
freqVec = freqSample*n/len(n) #Domain
freqVecS = freqVec[6999:-7000] #Tighten Domain for better plot
FyS = Fy[6999:-7000]

fig = plt.figure()
plt.plot(freqVecS, FyS, 'k', linewidth = 1.4)
plt.title("3-part Fourier Transform")
plt.xlabel('f [Hz]', fontsize=18)
plt.ylabel('|A(f)|', fontsize=18)
plt.grid()
plt.show()

#c)
yInv = np.real(fftP.ifft(fftP.ifftshift(FyRaw)))
yInv = yInv[:len(tSmall)]

fig = plt.figure()
plt.subplot(2, 1, 1)
plt.plot(tSmall, ySmall, 'b', linewidth = 1.4)
plt.title("Original Function")
plt.xlabel('t', fontsize=12)
plt.ylabel('A', fontsize=12)
plt.grid(1)

plt.subplot(2, 1, 2)
plt.plot(tSmall, yInv, 'r', linewidth = 1.4)
plt.title("Transformed and Inverted Function")
plt.xlabel('t', fontsize=12)
plt.ylabel('A', fontsize=12)
plt.grid(1)
plt.show()

#d)
def onpick(event):
    thisline = event.artist
    xdata = thisline.get_xdata()
    ydata = thisline.get_ydata()
    ind = event.ind
    points = tuple(zip(xdata[ind], ydata[ind]))
    print('Picked point:', points)

fig = plt.figure()
plt.plot(freqVec, Fy, 'ko', picker=5)
plt.title("Choose a Point")
plt.xlabel('f [Hz]', fontsize=18)
plt.ylabel('|A(f)|', fontsize=18)
fig.canvas.mpl_connect('pick_event', onpick)
plt.grid()
plt.show()

#e)
print("High points: ((-12.0, 0.8999999999999928),(12.0, 0.8999999999999928))")
indneg = list(freqVec).index(-12.)
indpos = list(freqVec).index(12.)
Fy[indneg] = 0
Fy[indpos] = 0

freqVecS = freqVec[6999:-7000] #Tighten Domain for better plot
FyS = Fy[6999:-7000]

fig = plt.figure()
plt.plot(freqVecS, FyS, 'k', linewidth = 1.4)
plt.title("Fourier Transform -12 Hz Signal")
plt.xlabel('f [Hz]', fontsize=18)
plt.ylabel('|A(f)|', fontsize=18)
plt.grid()
plt.show()

#f, g)
ySimp = amp1*np.sin(2*np.pi*freq1*tSmall)+amp2*np.sin(2*np.pi*freq2*tSmall)

FyRaw[indneg] = 0
FyRaw[indpos] = 0
ySimpInv = np.real(fftP.ifft(fftP.ifftshift(FyRaw)))
ySimpInv = ySimpInv[:len(tSmall)]

fig = plt.figure()
plt.subplot(2, 1, 1)
plt.plot(tSmall, ySimp, 'b', linewidth = 1.4)
plt.title("Original Function")
plt.xlabel('t', fontsize=12)
plt.ylabel('A', fontsize=12)
plt.grid(1)

plt.subplot(2, 1, 2)
plt.plot(tSmall, ySimpInv, 'r', linewidth = 1.4)
plt.title("Transformed and Inverted Function")
plt.xlabel('t', fontsize=12)
plt.ylabel('A', fontsize=12)
plt.grid(1)
plt.show()

#Question 3 -------------------------------------------

#See Attached Papers