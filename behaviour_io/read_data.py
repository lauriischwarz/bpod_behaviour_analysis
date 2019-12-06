import load_nested_structs as load_ns
from behaviour_io.constants import ROOT_FOLDER
from behaviour_io.get_data import get_settings, convert_raw_events_matlab_structs_to_dictionaries

import glob
import ntpath
import numpy as np
import warnings

warnings.filterwarnings('ignore')


def read_mouse_data_from_bpod(mouse_id, bpod_protocol_name, printout=True):
    """Reads all data from one animal and one protocol"""
    experiment_files = []
    experiment_data = []
    ntrials_distribution = []
    protocols = []
    stimulations = []
    muscimol = []

    mat_file_path = f"{ROOT_FOLDER}{mouse_id}{bpod_protocol_name}Session Data/*.mat"  # TODO: implement in pathlib
    filelist = glob.glob(mat_file_path)
    filelist.sort()

    for i, file_path in enumerate(filelist):
        data = load_ns.loadmat(file_path)

        if "nTrials" not in data["SessionData"]:
            continue

        muscimol, ntrials, protocol, stimulation = parse_data_settings(i, data, file_path, printout)

        ntrials_distribution.append(ntrials)
        protocols.append(protocol)
        stimulations.append(stimulation)
        muscimol.append(muscimol)

        trial_raw_events = data["SessionData"]["RawEvents"]["Trial"]
        try:
            trial_raw_events = convert_raw_events_matlab_structs_to_dictionaries(trial_raw_events)
        except Exception as e:
            print(e)
            trial_raw_events = None

        if trial_raw_events is not None:
            data["SessionData"]["RawEvents"]["Trial"] = trial_raw_events
        else:
            data["SessionData"]["RawEvents"]["Trial"] = np.nan

        experiment_data.append(data)

    return {  # TODO: implement as dictionary from beginning
            'experiment_files': experiment_files,
            'experiment_data': experiment_data,
            'ntrials_distribution': ntrials_distribution,
            'protocols': protocols,
            'stimulus': stimulations,
            'muscimol': muscimol,
    }


def parse_data_settings(counter, data, file_path, printout):

    if "SessionData" in data:
        ntrials = data["SessionData"]["nTrials"]

    trial_settings = data["SessionData"]["TrialSettings"]

    try:
        for trial_num, trial in enumerate(trial_settings):
            trial_settings[trial_num] = load_ns._todict(trial)
        data["SessionData"]["TrialSettings"] = trial_settings
    except:
        data["SessionData"]["TrialSettings"] = np.nan

    protocol = get_settings(trial_settings, "TrainingLevel")
    stimulation = get_settings(trial_settings, "OptoStim")
    muscimol = get_settings(trial_settings, "Muscimol")

    if printout:
        print(
            f"{counter}: {ntpath.basename(file_path)}, {ntrials} trials on {protocol}, stim {stimulation}, muscimol {muscimol}"
        )

    return muscimol, ntrials, protocol, stimulation

