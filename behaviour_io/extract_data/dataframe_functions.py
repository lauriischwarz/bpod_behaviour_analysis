import pathlib
import pandas as pd
from behaviour_io.extract_data import add_to_session_df
from behaviour_io.constants import EXP_CONDITION_DICTIONARY, ROOT_FOLDER
import numpy as np


def main(fname='dataframe_main.csv'):

    root_folder = pathlib.Path(ROOT_FOLDER)

# if you analyse new animals, uncomment the following two lines

    #for mid in MOUSE_ID_DICT.keys():
     #     generate_mouse_df(mid, fname, root_folder)

    fpaths = list(root_folder.glob(f"*{fname}"))
    dfs = []
    for fpath in fpaths:
        try:
            df = pd.read_csv(str(fpath))
            dfs.append(df)
        except Exception as e:
            print(e)
            print(fpath)
    all_df = add_to_session_df.merge_dataframes(dfs)

    all_df_trial_number = add_to_session_df.add_trial_number_to_df(all_df)
    all_df_ohda = add_to_session_df.add_exp_condition_to_df(all_df_trial_number, EXP_CONDITION_DICTIONARY)

    all_df_ohda.to_csv(f"{root_folder}/merged_dataframe.csv")


def n_trials_to_criterion(mid, df, criterion):
    mouse_df = df[df['animal_id'] == mid]
    at_criterion = mouse_df['cumulative_performance'] > criterion
    trial_idx_at_criterion = np.where(at_criterion)[0]
    for idx in trial_idx_at_criterion:
        if idx > 1500:
            return idx


def max_performance_reached(mid, df, limit=None):
    if limit is None:
        mouse_df = df[df['animal_id'] == mid]
        max_performance_reached = np.nanmax(mouse_df['cumulative_performance'])
    else:
        mouse_df = df[df['animal_id'] == mid]
        max_performance_reached = np.nanmax(mouse_df['cumulative_performance'][:limit])
    return max_performance_reached


def median_performance_reached_in_last_ntrials(mid, df, n_trials=500):
    mouse_df = df[df['animal_id'] == mid]
    max_performance_reached = np.nanmedian(mouse_df['cumulative_performance'][-n_trials:])
    return max_performance_reached


def performance_reached_at_control_finish(mid, df):
    control_mid = 'SomFlp06'
    control_df = df[df['animal_id'] == control_mid]
    max_perf_reached_ctrl = max_performance_reached(control_mid, control_df)
    trial_number_when_max_performance_reached = n_trials_to_criterion(control_mid, control_df, max_perf_reached_ctrl)

    max_pf_reached = max_performance_reached(mid, df, limit=trial_number_when_max_performance_reached)

    return max_pf_reached


def get_performance_summary_df(df, ohda_dict, task_label=3, criterion=80):
    summary = {}
    task_df = df[df['TrainingLevel'] == task_label]
    n_trials_to_criterion_result = []
    max_performance_result = []
    performance_cf_control = []
    median_performance_reached_in_last_ntrials_result = []

    for mid, group in ohda_dict.items():
        n_trials_to_criterion_result.append(n_trials_to_criterion(mid, task_df, criterion))
        max_performance_result.append(max_performance_reached(mid, task_df))
        performance_cf_control.append(performance_reached_at_control_finish(mid, task_df))
        median_performance_reached_in_last_ntrials_result.append(median_performance_reached_in_last_ntrials(mid, task_df))
    summary.setdefault('median_performance_reached_in_last_ntrials', median_performance_reached_in_last_ntrials_result)
    summary.setdefault('performance_cf_control', performance_cf_control)
    summary.setdefault('n trials to criterion', n_trials_to_criterion_result)
    summary.setdefault('max performance reached', max_performance_result)
    summary.setdefault('mouse id', list(ohda_dict.keys()))
    summary.setdefault('lesion condition', list(ohda_dict.values()))
    return pd.DataFrame.from_dict(summary)



if __name__ == '__main__':
    main()
