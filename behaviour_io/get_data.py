#%load_ext autoreload
#%autoreload 2
import os
import sys
from behaviour_io.read_data import ReadAnimalData
import custom_functions
sys.path.append("../")  # go to parent
import ntpath
import pandas as pd
import warnings

warnings.filterwarnings('ignore')

# Select animal to analyze
AnimalID = 'DRD103'
# Task
BpodProtocol = '/Two_Alternative_Choice/'
# Behavioural data
GeneralDirectory = '/Users/lauraschwarz/Documents/Bpod_raw/'

# Create out directory if it does not exist
outputDir = GeneralDirectory + AnimalID + BpodProtocol + 'Data_Analysis/'
if not os.path.isdir(outputDir):
    os.mkdir(outputDir)

ExperimentFiles, ExperimentData, ntrialsDistribution, Protocols, Stimulations, Muscimol =\
ReadAnimalData(GeneralDirectory, AnimalID, BpodProtocol, printout=True)

# get the date and time from the files
ExperimentTimes = custom_functions.ParseForTimes(ExperimentFiles)
ExperimentDates = custom_functions.ParseForDates(ExperimentFiles)
TimeDifferences = custom_functions.timeDifferences(ExperimentTimes)

# Transform to e.g. Feb20
ExperimentDatesPretty = custom_functions.MakeDatesPretty(ExperimentTimes)

# Clean data
# Remove those experiments fow which a proper time has not been found (old ones that are missing a lot of variables)
# Or those with low number of trials
minNoOfTr = 30
idxToRemove = custom_functions.identifyIdx(ExperimentTimes, ntrialsDistribution, minNoOfTr)

for idx in idxToRemove:
    print('deleting data for {} with {} trials'.format(ntpath.basename(ExperimentFiles[idx]), ntrialsDistribution[idx]))
    ExperimentData.pop(idx)
    ExperimentDates.pop(idx)
    ExperimentDatesPretty.pop(idx)
    ExperimentFiles.pop(idx)
    ExperimentTimes.pop(idx)
    ntrialsDistribution.pop(idx)
    Protocols.pop(idx)
    Stimulations.pop(idx)
    Muscimol.pop(idx)

# get all data into a dataframe
DataFrames = [custom_functions.SessionDataToDataFrame(AnimalID, ExperimentDatesPretty[i], exp['SessionData'])
              for i, exp in enumerate(ExperimentData)]

AnimalDF = pd.concat(DataFrames, ignore_index=True)

# save the dataframe
AnimalDF.to_csv(outputDir + AnimalID + '_dataframe.csv')

print(AnimalDF.keys())