import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
from behaviour_io.merge_dataframes_of_animals import merge_DF

# Select animal to analyze
AnimalID = 'DRD103'
# Task
BpodProtocol = '/Two_Alternative_Choice/'
# Behavioural data
GeneralDirectory = '/Users/lauraschwarz/Documents/Bpod_raw/'

# Create out directory if it does not exist
outputDir = GeneralDirectory + AnimalID + BpodProtocol + 'Data_Analysis/'

# read data like this:
AnimalDF = pd.read_pickle(outputDir + AnimalID + '_dataframe.pkl')
print(AnimalDF.keys())
fig, ax = plt.subplots(figsize=(15,5))
ax.axhline(50, ls='--', alpha=0.4, color='k')
ax.axhline(100, ls='--', alpha=0.4, color='k')
sns.lineplot(x=AnimalDF.index, y='CumulativePerformance', hue='Protocol', data=AnimalDF, markers=".", linewidth=0.3)

plt.show()

sns.barplot(x="SessionTime", y='TrialIndex', hue='Protocol', data=AnimalDF)

plt.show()

AnimalID_list = ["D1cre06", "D1cre01", "DRD101", "D1cre02", "D1cre03", "D1cre05", "D1cre04", "DRD103", "DRD102"]
Animal_group_list = ['D1Caspase', 'D1Caspase', 'D1Caspase', 'D1Caspase', 'D1Caspase', 'D1Caspase', 'CTXBuffer',
                       'CTXBuffer', 'CTXBuffer']

Animals_merged_DF = merge_DF(AnimalID_list)
Animals_merged_DF['Injection'] = Animals_merged_DF.apply(merge_DF, axis=1)

print(Animals_merged_DF.AnimalID)
#
#fig, ax = plt.subplots(figsize=(15, 5))
#ax.axhline(50, ls='--', alpha=0.4, color='k')
#ax.axhline(100, ls='--', alpha=0.4, color='k')
#sns.lineplot(x=Animals_merged_DF.index, y='CumulativePerformance', hue='AnimalID', data=Animals_merged_DF, markers=".", linewidth=0.3)

#plt.show()

