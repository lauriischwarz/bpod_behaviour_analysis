import load_nested_structs as load_ns
from behaviour_io.constants import ROOT_FOLDER
from behaviour_io import get_data

import glob
import ntpath
import numpy as np
import warnings

warnings.filterwarnings('ignore')


def read_mouse_data_from_bpod(mouse_id, bpod_protocol_name, printout=True):
    """Reads all data from one animal and one protocol"""

    mat_file_path = f"{ROOT_FOLDER}{mouse_id}{bpod_protocol_name}Session Data/*.mat"  # TODO: implement with pathlib
    filelist = glob.glob(mat_file_path)
    filelist.sort()
    prev_session = None

    for i, file_path in enumerate(filelist):
        data = load_ns.loadmat(file_path)

        if "nTrials" in data["SessionData"]:  # FIXME:
            # assumes first trial represents all future trials in a session

            session_settings = parse_session_settings(i, data, file_path, printout)
            trial_raw_events = data["SessionData"]["RawEvents"]["Trial"]

            try:
                trial_raw_events = get_data.convert_raw_events_matlab_structs_to_dictionaries(trial_raw_events)
            except Exception as e:
                print(e)
                trial_raw_events = None

            if trial_raw_events is not None:
                data["SessionData"]["RawEvents"]["Trial"] = trial_raw_events
            else:
                data["SessionData"]["RawEvents"]["Trial"] = np.nan

            session_settings['experiment_data'] = [data]
            session_settings['experiment_files'] = [filelist]

            if prev_session is not None:
                merge_dictionaries(session_settings, prev_session)

            prev_session = session_settings

    return session_settings


def parse_session_settings(counter, data, file_path, printout):

    raw_settings = data["SessionData"]["TrialSettings"]

    processed_settings = [load_ns._todict(t) for t in raw_settings]

    session_settings = get_data.read_trial_settings(processed_settings, 0)
    session_settings.setdefault('nTrials', [data["SessionData"]["nTrials"]])

    if printout:
        print(
            f"{counter}: {ntpath.basename(file_path)}, {list(item for item in session_settings.items())}"
        )
    return session_settings


def merge_dictionaries(this_dict, other):
    for key, value in this_dict.items():
        value.extend(other[key])
    return this_dict


def get_trial_data_from_session(session_data):
    trial_data_raw = session_data["RawEvents"]["Trial"]
    states = []
    events = []

    for trial in trial_data_raw:
        states.extend(trial['States'])
        events.extend(trial['Events'])
    return states, events
