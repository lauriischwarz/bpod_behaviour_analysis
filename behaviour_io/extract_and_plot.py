import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
from behaviour_io.constants import ROOT_FOLDER, BPOD_PROTOCOL


# Select animal to analyze
AnimalID = 'DRD103'
# Task
BpodProtocol = '/Two_Alternative_Choice/'
# Behavioural data
GeneralDirectory = '/Users/lauraschwarz/Documents/Bpod_raw/'

# Create out directory if it does not exist
outputDir = GeneralDirectory + AnimalID + BpodProtocol + 'Data_Analysis/'

# read data like this:
AnimalDF = pd.read_csv(outputDir + AnimalID + '_dataframe.csv')
print(AnimalDF.keys())
fig, ax = plt.subplots(figsize=(15,5))
ax.axhline(50, ls='--', alpha=0.4, color='k')
ax.axhline(100, ls='--', alpha=0.4, color='k')
sns.lineplot(x=AnimalDF.index, y='CumulativePerformance', hue='Protocol', data=AnimalDF, markers=".", linewidth=0.3)

plt.show()

sns.barplot(x="SessionTime", y='TrialIndex', hue='Protocol', data=AnimalDF)

plt.show()

bpod_protocol = BPOD_PROTOCOL
output_dir = f'{ROOT_FOLDER}{bpod_protocol}Data_Analysis/'
merged_df = pd.read_csv(f"{output_dir}_merged_dataframe.csv")
sns.lineplot(x='TrialIndex',
             y='CumulativePerformance',
             hue='AnimalID',
             data=merged_df,
             markers=".",
             linewidth=0.3,
             err_style=None)

plt.show()
#
#fig, ax = plt.subplots(figsize=(15, 5))
#ax.axhline(50, ls='--', alpha=0.4, color='k')
#ax.axhline(100, ls='--', alpha=0.4, color='k')
#sns.lineplot(x=Animals_merged_DF.index, y='CumulativePerformance', hue='AnimalID', data=Animals_merged_DF, markers=".", linewidth=0.3)

#plt.show()

