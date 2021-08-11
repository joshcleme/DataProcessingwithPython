import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


##### Replicate these lines in Python console

# read in file with better column names
signalBR = pd.read_csv('VP02/BitalinoBR.csv', usecols=[0])
signalECG = pd.read_csv('VP02/BitalinoECG.csv', usecols=[0])


#pull out the V5 signal
BR = signalBR.to_numpy()
BR=np.delete(BR, -1)
ECG = signalECG.to_numpy()
ECG=np.delete(ECG, -1)


### pass data through LOW PASS FILTER (fs=250Hz, fc=15, N=6) ###
low_passBR = np.convolve(BR, [0.023834522, 0.093047634, 0.232148599, 0.301938491, 0.232148599, 0.093047634, 0.023834522])
low_passECG = np.convolve(ECG, [0.023834522, 0.093047634, 0.232148599, 0.301938491, 0.232148599, 0.093047634, 0.023834522])

### pass data through HIGH PASS FILTER (fs=250Hz, fc=5Hz, N=6) to create BAND PASS result ###
band_passBR = np.convolve(low_passBR, [-0.000798178, -0.003095487, -0.007692586, 0.989209446, -0.007692586, -0.003095487, -0.000798178])
band_passECG = np.convolve(low_passECG, [-0.000798178, -0.003095487, -0.007692586, 0.989209446, -0.007692586, -0.003095487, -0.000798178])

### pass data through weighter differiator
diffBR = np.convolve(band_passBR, [1, 2, -2, -1])   #I think this is incorrect as it does not look "forward" but should work
diffECG = np.convolve(band_passECG, [1, 2, -2, -1])   #I think this is incorrect as it does not look "forward" but should work

## pass data through square function
squaredBR = diffBR * diffBR
squaredECG = diffECG * diffECG

## pass through moving average of 150ms window @ 250 Hz => 38 samples
weights = np.ones(38)

averageBR = np.convolve(squaredBR, weights)
averageECG = np.convolve(squaredECG, weights)

onelst = []
onelst.extend([1/150] * 150)
movingavgBR = np.convolve(averageBR, onelst)
movingavgECG = np.convolve(averageECG, onelst)

del onelst[0]
movingavgBR = np.insert(movingavgBR, 0, onelst)
movingavgECG = np.insert(movingavgECG, 0, onelst)
onelst.extend([1] * 149)
averageBR = np.append(averageBR, onelst)
averageECG = np.append(averageECG, onelst)

spacer = []
one = 1
index = []
i = 0
while i < 149:
    index.append(i)
    spacer.append(one)
    i = i + 1

movingavgBR = np.delete(movingavgBR, index)
movingavgBR = np.append(movingavgBR, spacer)

print(len(averageBR))
print(len(averageECG))
print(len(movingavgBR))
print(len(movingavgECG))

start = 1900
window = 0.005
anxietysignaturesBR = []
w=1900
while w < len(averageBR) - start:
    if averageBR[w] >= (movingavgBR[w] - window) and averageBR[w] <= (movingavgBR[w] + window):
        anxietysignaturesBR.append(w)
    w = w + 1
print(len(anxietysignaturesBR))
print(anxietysignaturesBR)

anxietysignaturesECG = []
q=1900
while q < len(averageECG) - start:
    if averageECG[q] >= (movingavgECG[q] - window) and averageECG[q] <= (movingavgECG[q] + window):
        anxietysignaturesECG.append(q)
    q = q + 1

print(len(anxietysignaturesECG))
print(anxietysignaturesECG)


#plt.plot(averageBR)
#plt.title('Averaged')
#plt.show()
