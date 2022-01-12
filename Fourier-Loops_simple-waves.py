#Earth Science 131
#UCSB Winter 2019, Professor Matoza
#Lab 1: Fourier series
#James Danbury

import numpy as np
import matplotlib.pyplot as plt

#Question 1: Plotting a square wave using truncated Fourier series
dt = .01
t = np.arange(-np.pi, np.pi+dt, dt)

print('Calculating Fourier series for square...')
n = 3
while(True):
    TruncFourier = np.zeros(shape=(len(t),n))
    i = 1
    while(i <= n):
        TruncFourier[:,i-1] = (1/(2*i-1))*np.sin((2*i-1)*t)
        i = i+1
    y = 4/np.pi * np.sum(TruncFourier, axis=1)
    if(n == 3):
        Yn3 = y
        n = 5
    elif (n == 5):
        Yn5 = y
        n = 10
    elif (n == 10):
        Yn10 = y
        n = 50
    elif (n == 50):
        Yn50 = y
        n = 500
    else:
        break

print('Plotting square wave!')
plt.plot(t,Yn3,'r',linewidth = 1.4)
plt.plot(t,Yn5,'orange',linewidth = 1.4)
plt.plot(t,Yn10,'y',linewidth = 1.4)
plt.plot(t,Yn50,'g',linewidth = 1.4)
plt.plot(t,y,'b',linewidth = 1.4)
plt.xlim(t[0],t[-1])
plt.xlabel('Time')
plt.ylabel('Value')
plt.title('Fourier Series Result for Odd Square Wave')
plt.legend(['N=3','N=5','N=10','N=50','N=500'])
plt.grid()
plt.show()

#Question 2: Plotting a sawtooth wave using truncated Fourier series
#b) sawtooth with 2pi
P = 2*np.pi
name = "Fourier Series Result for Odd Sawtooth Wave With Period of Two pi"
dt = .01
while(True):
    t = np.arange(-P/2, P/2+dt, dt)
    print('Calculating Fourier series for sawtooth...')
    n = 3
    while(True):
        TruncFourier = np.zeros(shape=(len(t),n))
        i = 1
        while(i <= n):
            if(P == 2*np.pi):
                TruncFourier[:,i-1] = (2/i)*(-1**(i-1))*np.sin(i*t)
            else:
                TruncFourier[:,i-1] = ((2*P)/(i*np.pi))*(-1**(i-1))*np.sin((2*np.pi*i*t)/P)
            i = i+1
        y = np.sum(TruncFourier, axis=1)
        if(n == 3):
            Yn3 = y
            n = 5
        elif (n == 5):
            Yn5 = y
            n = 10
        elif (n == 10):
            Yn10 = y
            n = 50
        elif (n == 50):
            Yn50 = y
            n = 500
        else:
            break

    print('Plotting Sawtooth!')
    plt.plot(t,Yn3,'r',linewidth = 1.4)
    plt.plot(t,Yn5,'orange',linewidth = 1.4)
    plt.plot(t,Yn10,'y',linewidth = 1.4)
    plt.plot(t,Yn50,'g',linewidth = 1.4)
    plt.plot(t,y,'b',linewidth = 1.4)
    plt.xlim(t[0],t[-1])
    plt.xlabel('Time')
    plt.ylabel('Value')
    plt.title(name)
    plt.legend(['N=3','N=5','N=10','N=50','N=500'])
    plt.grid()
    plt.show()

    if(P == 2*np.pi):     #c) Sawtooth with generalized period
        P = 10
        name = "Fourier Series Result for Odd Sawtooth Wave with Period of 10 seconds"
    elif(P == 10):
        P = 250
        dt = .1
        name = "Fourier Series Result for Odd Sawtooth Wave with Period of 250 seconds"
    else:
        break
#d) Sawtooth periodic function expanded

print('Calculating Fourier series for sawtooth...')
t = np.arange(-4*P, 4*P+dt, dt)
n = 50
TruncFourier = np.zeros(shape=(len(t),n))
i = 1
while(i <= n):
    TruncFourier[:,i-1] = ((2*P)/(i*np.pi))*(-1**(i-1))*np.sin((2*np.pi*i*t)/P)
    i = i+1
y = np.sum(TruncFourier, axis=1)

print('Plotting expanded sawtooth!')
plt.plot(t,y,'b',linewidth = 1.4)
plt.xlim(t[0],t[-1])
plt.xlabel('Time')
plt.ylabel('Value')
plt.title(name)
plt.grid()
plt.show()