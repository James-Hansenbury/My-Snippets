import numpy as np

print("This program will give the confidence interval with a given set of input values.")

t = float(input("Input value for t distribution: "))
print("Input values of the sample group for requested interval separated by spaces:")
samples = [float(x) for x in input().split()]
while(len(samples) <= 1):
    print("Need at least 2 values in the group, input them again:")
    samples = [int(x) for x in input().split()]

n = len(samples)
mean = np.average(samples)
print("Average of samples is: ", mean)

s = np.sqrt(1/(n-1)*np.sum((samples-mean)**2))
print("Standard deviation is approximately: ", s)

minConf = mean-t*(s/np.sqrt(n))
maxConf = mean+t*(s/np.sqrt(n))
print("The confidence interval is:")
print(minConf, " <= mu <= ", maxConf)