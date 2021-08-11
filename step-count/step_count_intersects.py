import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

##### Replicate these lines in Python console

# read in file with better column names
signal = pd.read_csv('p2.2_Male_20-29_180-189cm_Hand_held.out.csv', names=['time', 'accel_x', 'accel_y', 'accel_z', 'gyro_x', 'gyro_y', 'gyro_z', 'mag_x', 'mag_y', 'mag_z'])

# drop the bad data in rows 0 and 1
signal = signal.drop([0])

# set the correct types
signal = signal.astype({'time': 'float32', 'accel_x': 'float32'})

#pull out the V5 signal
pos = signal['accel_x'].to_numpy()

### pass data through LOW PASS FILTER (fs=250Hz, fc=15, N=6) ###
low_pass = np.convolve(pos, [0.023834522, 0.093047634, 0.232148599, 0.301938491, 0.232148599, 0.093047634, 0.023834522])

### pass data through HIGH PASS FILTER (fs=250Hz, fc=5Hz, N=6) to create BAND PASS result ###
band_pass = np.convolve(low_pass, [-0.000798178, -0.003095487,-0.007692586, 0.989209446, -0.007692586, -0.003095487, -0.000798178])

### pass data through weighter differiator
diff = np.convolve(band_pass,[1,2,-2,-1])   #I think this is incorrect as it does not look "forward" but should work

## pass data through square function
squared = diff * diff

## pass through moving average of 150ms window @ 250 Hz => 38 samples
weights = np.ones(38)
average = np.convolve(squared, weights)


onelst = []
onelst.extend([1/150] * 150)
averagegraph = np.convolve(average, onelst)
#plt.plot(average)
#plt.title('Averaged')
#plt.show()

del onelst[0]
averagegraph = np.insert(averagegraph, 0, onelst)
onelst.extend([1] * 149)
average = np.append(average, onelst)
#print(len(averagegraph))
#print(len(average))


spacer = []
one = 1
index = []
i = 0
while i < 149:
    index.append(i)
    spacer.append(one)
    i = i + 1

averagegraph = np.delete(averagegraph, index)
averagegraph = np.append(averagegraph, spacer)


plt.plot(average)
plt.plot(averagegraph)
plt.title('Testing Testing')
plt.show()

avg = sum(average)/len(average)

walkingtimecounter = 0
aretheywalking = 0
q=0
while q < len(average):
    if average[q] < avg:
        walkingtimecounter = walkingtimecounter + 1
    elif average[q] > avg:
        walkingtimecounter = 0
    if walkingtimecounter > 100:
        aretheywalking = 1
    q = q + 1

intersect_count = 0
w=1900
while w < len(average) - 1900:
    if average[w] >= (averagegraph[w] - 0.75) and average[w] <= (averagegraph[w] + 0.75):
        intersect_count = intersect_count + 1
    w = w + 1


stepcount = intersect_count//2

print("There are " + str(stepcount) + " steps in this walk")