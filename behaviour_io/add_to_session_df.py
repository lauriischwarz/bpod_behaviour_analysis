import pathlib

import numpy as np
import pandas as pd

from behaviour_io.constants import ROOT_FOLDER, BPOD_PROTOCOL
from behaviour_io.load_data_from_matfile_to_df import loadmat, import_data_to_python, extract_trial_settings, \
    combine_dictionaries, get_events_and_state, get_list, extract_from_dict


def add_cumulative_performance_to_session_df(df):
    first_poke_correct = df['FirstPokeCorrect']
    correct_cp = np.cumsum(first_poke_correct == 1)
    incorrect_cp = np.cumsum(first_poke_correct == 0)
    cumulative_performance = 100 * correct_cp / (correct_cp + incorrect_cp)
    df['cumulative_performance'] = cumulative_performance
    df['cumulative_performance'].iloc[0:int(len(df)/20)+1] = np.nan
    percent_correct = np.nanmedian(cumulative_performance)
    df['percent_correct'] = percent_correct
    return df


def change_key_in_traininglevel(file_path):
    pass


def add_trial_number_to_df(merged_df):
    merged_df['trial_number'] = np.full(len(merged_df), np.nan)

    for mid in merged_df['animal_id'].unique():
        for protocol in merged_df['TrainingLevel'].unique():
            conditions = np.logical_and(merged_df['animal_id'] == mid,
                                        merged_df['TrainingLevel'] == protocol)
            conditions_locs = merged_df[conditions].index

            merged_df.trial_number.loc[conditions_locs] = \
                np.arange(len(merged_df[conditions])) + 1

    return merged_df


def add_exp_condition_to_df(merged_df, EXP_CONDITION_DICTIONARY):
    merged_df['experimental_condition'] = np.full(len(merged_df), np.nan)

    for (k, v) in EXP_CONDITION_DICTIONARY.items():
        this_mouse = merged_df['animal_id'] == k
        merged_df['experimental_condition'][this_mouse] = v

    return merged_df


def merge_dataframes(dfs):
    df_all = pd.concat(dfs, ignore_index=True, sort=True)
    return df_all


def generate_mouse_df(mouse_id, fname, root_folder):
    main_df = pd.DataFrame()

    mat_file = f"{root_folder}/{mouse_id}/{BPOD_PROTOCOL}/Session Data/"
    mat_file_path = pathlib.Path(mat_file)
    all_mat_files = list(mat_file_path.glob('*.mat'))

    for i, file_path in enumerate(all_mat_files):
        session_df = extract_session(file_path, save=True)
        if session_df is not None:
            session_df['session_id'] = [i] * len(session_df)
            session_df_with_cumulative_performance = add_cumulative_performance_to_session_df(session_df)
            main_df = main_df.append(session_df_with_cumulative_performance, ignore_index=True)

    main_df['animal_id'] = np.full(len(main_df), mouse_id)
    main_df.to_csv(f"{root_folder}/{mouse_id}_{fname}", index=False)


def extract_session(file_path, save=True):
    df_dict = {}
    matlab_data = loadmat(file_path)['SessionData']
    python_data = import_data_to_python(matlab_data)

    if 'nTrials' in python_data.keys():
        trial_settings = extract_trial_settings(python_data)
        combine_dictionaries(trial_settings, df_dict)
        n_trials = python_data['nTrials']
        session_timestamp = [str(file_path).split('_')[-2]]*n_trials


        for k, v in python_data.items():

            if k in ['Stimulus', 'GitHash', 'Info', 'RawData']:
                continue

            if k == 'RawEvents':
                events, _ = get_events_and_state(v)
                combine_dictionaries(events, df_dict)

            if isinstance(v, np.ndarray):
                df_dict.setdefault(k, get_list(v, n_trials))

            elif isinstance(v, dict):
                extract_from_dict(n_trials, v, df_dict)
        df_dict.setdefault('session date', session_timestamp)

        df = pd.DataFrame.from_dict(df_dict)
        if save:
            df.to_csv(str(file_path).replace('.mat', '.csv'), index=False)
        return df
