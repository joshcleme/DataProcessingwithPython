import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import find_peaks

##### Replicate these lines in Python console

# read in file with better column names
signal = pd.read_csv('nstdb_118e00.csv', names=['time', 'ml2', 'v5'])

# drop the bad data in rows 0 and 1
signal = signal.drop([0, 1])

# set the correct types
signal = signal.astype({'ml2': 'float32', 'v5': 'float32'})

#pull out the V5 signal
v5 = signal['v5'].to_numpy()

### pass data through LOW PASS FILTER (fs=250Hz, fc=15, N=6) ###
low_pass = np.convolve(v5, [0.023834522, 0.093047634, 0.232148599, 0.301938491, 0.232148599, 0.093047634, 0.023834522])

### pass data through HIGH PASS FILTER (fs=250Hz, fc=5Hz, N=6) to create BAND PASS result ###
band_pass = np.convolve(low_pass, [-0.000798178, -0.003095487,-0.007692586, 0.989209446, -0.007692586, -0.003095487, -0.000798178])

### pass data through weighter differiator
diff = np.convolve(band_pass,[1,2,-2,-1])   #I think this is incorrect as it does not look "forward" but should work

## pass data through square function
squared = diff * diff

## pass through moving average of 150ms window @ 250 Hz => 38 samples
weights = np.ones(38)
average = np.convolve(squared, weights)

#plt.plot(average)
#plt.title('Averaged')
#plt.show()

avg = (sum(average[50:(len(average) - 50)])) / (len(average))

def findpeaks(arr, h=avg, w=7):
    peak = find_peaks(arr, height=h, width=w)
    peak_list = dict(zip(peak[0], peak[1]['peak_heights']))

    heights = list(peak_list.values())
    indices = list(peak_list.keys())
    difflst = []
    i = 1
    while i < len(indices):
        q = (indices[i] - indices[i - 1])
        difflst.append(q)
        if difflst[i - 1] < 60:
            del indices[i - 1]
            del heights[i - 1]
        i = i + 1
    print(len(indices))
    print(indices)
    return heights, indices


print(findpeaks(average))


