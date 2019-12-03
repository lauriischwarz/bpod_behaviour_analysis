#%load_ext autoreload
#%autoreload 2
import os
import sys

from behaviour_io.constants import ROOT_FOLDER, BPOD_PROTOCOL
from behaviour_io.read_data import ReadAnimalData
import custom_functions
sys.path.append("../")  # go to parent
import ntpath
import pandas as pd
import warnings

warnings.filterwarnings('ignore')

# Select animal to analyze


def extract_mouse(animal_id=''):
    output_dir = get_output_directory()

    if not os.path.isdir(output_dir):
        os.mkdir(output_dir)
    experiment_files, experiment_data, ntrials_distribution, protocols, stimulations, muscimol = \
        ReadAnimalData(ROOT_FOLDER, animal_id, BPOD_PROTOCOL, printout=True)
    ExperimentTimes = custom_functions.ParseForTimes(experiment_files)
    ExperimentDates = custom_functions.ParseForDates(experiment_files)
    ExperimentDatesPretty = custom_functions.MakeDatesPretty(ExperimentTimes)


    # Clean data
    # Remove those experiments fow which a proper time has not been found (old ones that are missing a lot of variables)
    # Or those with low number of trials
    minNoOfTr = 30
    idxToRemove = custom_functions.identifyIdx(ExperimentTimes, ntrials_distribution, minNoOfTr)
    for idx in idxToRemove:
        print('deleting data for {} with {} trials'.format(ntpath.basename(experiment_files[idx]),
                                                           ntrials_distribution[idx]))
        experiment_data.pop(idx)
        ExperimentDates.pop(idx)
        ExperimentDatesPretty.pop(idx)
        experiment_files.pop(idx)
        ExperimentTimes.pop(idx)
        ntrials_distribution.pop(idx)
        protocols.pop(idx)
        stimulations.pop(idx)
        muscimol.pop(idx)
    # get all data into a dataframe
    DataFrames = [custom_functions.SessionDataToDataFrame(animal_id, ExperimentDatesPretty[i], exp['SessionData'])
                  for i, exp in enumerate(experiment_data)]
    AnimalDF = pd.concat(DataFrames, ignore_index=True)
    # save the dataframe
    AnimalDF.to_csv(output_dir + animal_id + '_dataframe.csv')
    print(AnimalDF.keys())


def get_output_directory():
    return f'{ROOT_FOLDER}{animal_id}{bpod_protocol}Data_Analysis/'


mouse_ids = ["D1cre06", "D1cre01", "DRD101", "D1cre02", "D1cre03", "D1cre05", "D1cre04", "DRD103", "DRD102"]
for m_id in mouse_ids:
    extract_mouse(m_id)
