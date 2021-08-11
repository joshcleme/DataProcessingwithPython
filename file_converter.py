# importing panda library
import pandas as pd
n=80

# readinag given csv file
# and creating dataframe
dataframe1 = pd.read_csv("VP02/BitalinoBR.txt", delimiter = '\t')
#dataframe2 = pd.read_csv("VP" + str(n) + "/BitalinoECG.txt", delimiter = '\t')
#dataframe3 = pd.read_csv("VP" + str(n) + "/BitalinoGSR.txt", delimiter = '\t')
# storing this dataframe in a csv file
dataframe1.to_csv('VP02/BitalinoBR.csv', index=None)
#dataframe2.to_csv('VP' + str(n) + '/BitalinoECG.csv', index=None)
#dataframe3.to_csv('VP' + str(n) + '/BitalinoGSR.csv', index=None)
