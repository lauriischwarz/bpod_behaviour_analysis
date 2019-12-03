import custom_functions
import load_nested_structs as load_ns
import ntpath
import pandas as pd


def get_settings(trial_settings, key):
    if key in trial_settings[0]["GUIMeta"]:
        return trial_settings[0]["GUIMeta"][key]["String"][trial_settings[0]["GUI"][key] - 1]
    return "unknown"


def convert_raw_events_to_dictionaries(trial_raw_events):
    for i, trial in enumerate(trial_raw_events):
        trial_raw_events[i] = load_ns._todict(trial)
    return trial_raw_events

def clean_data(ExperimentData, ExperimentDates, ExperimentDatesPretty, ExperimentTimes, ExperimentFiles, ntrialsDistribution, Protocols, Stimulations, Muscimol):
    # Clean data
    # Remove those experiments fow which a proper time has not been found (old ones that are missing a lot of variables)
    # Or those with low number of trials
    minNoOfTr = 30
    idxToRemove = custom_functions.identifyIdx(ExperimentTimes, ntrialsDistribution, minNoOfTr)

    for idx in idxToRemove:
        print('deleting data for {} with {} trials'.format(ntpath.basename(ExperimentFiles[idx]),
                                                           ntrialsDistribution[idx]))
        ExperimentData.pop(idx)
        ExperimentDates.pop(idx)
        ExperimentDatesPretty.pop(idx)
        ExperimentFiles.pop(idx)
        ExperimentTimes.pop(idx)
        ntrialsDistribution.pop(idx)
        Protocols.pop(idx)
        Stimulations.pop(idx)
        Muscimol.pop(idx)

def Data_to_Dataframe(AnimalID, ExperimentDatesPretty, ExperimentData):
    # get all data into a dataframe
    DataFrames = [custom_functions.SessionDataToDataFrame(AnimalID, ExperimentDatesPretty[i], exp['SessionData'])
                  for i, exp in enumerate(ExperimentData)]

    AnimalDF = pd.concat(DataFrames, ignore_index=True)

    print(AnimalDF.keys())

def session_to_remove(AnimalDF):
    # Select indexes to remove and remove them
    removesession = []

    IDsToRemove = []  # do not write here
    for counter, session in enumerate(pd.unique(AnimalDF['SessionTime'])):
        if counter in removesession:
            print(session + ' Removed')
            IDsToRemove.append(session)

    AnimalDF = AnimalDF.loc[~AnimalDF['SessionTime'].isin(IDsToRemove)]