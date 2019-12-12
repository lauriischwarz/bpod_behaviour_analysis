import os

import load_nested_structs as load_ns
from behaviour_io.constants import ROOT_FOLDER, BPOD_PROTOCOL, MIN_N_TRIALS
from behaviour_io.read_data import read_mouse_data_from_bpod
import custom_functions
import pandas as pd


def extract_mouse(mouse_id=''):
    output_dir = get_output_directory(mouse_id)

    if not os.path.isdir(output_dir):
        os.mkdir(output_dir)
    data = read_mouse_data_from_bpod(mouse_id, BPOD_PROTOCOL, printout=True)
    experiment_times = custom_functions.ParseForTimes(data['experiment_files'])
    experiment_dates_pretty = custom_functions.MakeDatesPretty(experiment_times)

    data = remove_unwanted_values_from_data(data, experiment_times)
    dfs = [custom_functions.session_to_df(mouse_id,
                                          experiment_dates_pretty[i],
                                          exp['SessionData']) for i, exp in enumerate(data['experiment_data'])]

    if len(dfs) > 1:
        mouse_df = pd.concat(dfs, ignore_index=True)
    else:
        mouse_df = dfs

    save_path = f"{output_dir}{mouse_id}_dataframe_new.csv"
    mouse_df.to_csv(save_path)
    print(mouse_df.keys())


def get_output_directory(animal_id):
    return f'{ROOT_FOLDER}{animal_id}{BPOD_PROTOCOL}Data_Analysis/'


def read_trial_settings(trial_settings, idx):
    gui_meta_trial_settings = trial_settings[idx]['GUIMeta']
    gui_settings_dict = {}

    for trial_setting_lbl in gui_meta_trial_settings.keys():
        if 'String' in gui_meta_trial_settings[trial_setting_lbl].keys():
            gui_option_selected_idx = trial_settings[0]["GUI"][trial_setting_lbl] - 1
            trial_setting = gui_meta_trial_settings[trial_setting_lbl]["String"][gui_option_selected_idx]
            gui_settings_dict.setdefault(trial_setting_lbl, [trial_setting])
        else:
            gui_settings_dict.setdefault(trial_setting_lbl, ['unknown'])
    return gui_settings_dict


def convert_raw_events_matlab_structs_to_dictionaries(trial_raw_events):
    for i, trial in enumerate(trial_raw_events):
        trial_raw_events[i] = load_ns._todict(trial)
    return trial_raw_events


def remove_unwanted_values_from_data(data, experiment_times):
    idx_to_remove = custom_functions.get_unwanted_idx(experiment_times,
                                                      data['nTrials'],
                                                      MIN_N_TRIALS)
    for k, v in data.items():
        new_d = [val for i, val in enumerate(v) if i not in idx_to_remove]  # TODO: check that this doesn't have deletion issues in the loop
        data[k] = new_d
    return data


def Data_to_Dataframe(AnimalID, ExperimentDatesPretty, ExperimentData):
    # get all data into a dataframe
    DataFrames = [custom_functions.session_to_df(AnimalID, ExperimentDatesPretty[i], exp['SessionData'])
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


def extract_all_mice(mouse_ids=("D1cre06", "D1cre01", "DRD101", "D1cre02", "D1cre03", "D1cre05", "D1cre04", "DRD103",
                           "DRD102")):
    for m_id in mouse_ids:
        extract_mouse(m_id)


extract_all_mice()
