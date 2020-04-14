import scipy.io
import numpy as np


def loadmat(filename):
    '''
    this function should be called instead of direct spio.loadmat
    as it cures the problem of not properly recovering python dictionaries
    from mat files. It calls the function check keys to cure all entries
    which are still mat-objects
    '''
    data = scipy.io.loadmat(filename, struct_as_record=False, squeeze_me=True)
    return _check_keys(data)


def _check_keys(data):
    for key in data:
        if isinstance(data[key], scipy.io.matlab.mio5_params.mat_struct):
            data[key] = _todict(data[key])
    return data


def _todict(matobj):
    matobj_as_dict = {}
    for key in matobj._fieldnames:
        val = matobj.__dict__[key]
        if isinstance(val, scipy.io.matlab.mio5_params.mat_struct):
            matobj_as_dict[key] = _todict(val)
        else:
            matobj_as_dict[key] = val
    return matobj_as_dict


def import_data_to_python(session_dict):
    for k, v in session_dict.items():
        new_v = check_for_matstructs(v)
        if new_v is not None:
            session_dict[k] = new_v
    return session_dict


def check_for_matstructs(item):
    if isinstance(item, np.ndarray):
        if any(isinstance(x, scipy.io.matlab.mio5_params.mat_struct) for x in item):
            return [_todict(matobj) for matobj in item]
        else:
            return item
    elif isinstance(item, dict):
        for k, v in item.items():
            item[k] = check_for_matstructs(v)


def get_list(item, n_trials):
    return item[:n_trials]


def extract_from_dict(n_trials, dict_in, dict_out):
    """takes nested dictionary and returns k v pairs
     for all items that are ntrials long"""
    for k, v in dict_in.items():
        if k == 'Trial':
            continue
        if v is None:
            continue
            #print(f'skipping: {k} ')
        elif len(v) == n_trials:
            #print(f'adding {k}')
            dict_out.setdefault(k, v)
        else:
            continue
            #print(f'skipping: {k} ')


def get_all_event_keys(all_trials):
    all_keys = []
    for t in all_trials:
        all_keys.extend(list(t['Events'].keys()))
    return list(set(all_keys))


def get_events_and_state(v):
    states = []
    all_trials = v['Trial']
    event_keys = get_all_event_keys(all_trials)
    events_dict = {k: [] for k in event_keys}

    for t in all_trials:
        states.append(t['States'])
        current_events_dict = get_event_numbers_from_trial(t, event_keys)

        for k, v in current_events_dict.items():
            events_dict[k].append(v)

    return events_dict, states


def get_event_numbers_from_trial(t, keys):
    new_dict = {}

    for k, v in t['Events'].items():
        if isinstance(v, int):
            v = [v]
        elif isinstance(v, float):
            v = [v]
        new_dict.setdefault(k, len(list(v)))

    for k in keys:
        if k not in t['Events'].keys():
            new_dict.setdefault(k, 0)
    return new_dict


def get_all_gui_keys(all_trials):
    all_keys = []
    for t in all_trials:
        all_keys.extend(list(t['GUI'].keys()))
    return list(set(all_keys))


def extract_trial_settings(data):
    trials = data['TrialSettings']
    gui_keys = get_all_gui_keys(trials)
    events_dict = {k: [] for k in gui_keys}

    for t in trials:
        for k, v in t['GUI'].items():
            events_dict[k].append(v)
    return events_dict


def combine_dictionaries(dictionary_to_add, dictionary_to_add_to):
    for k, v in dictionary_to_add.items():
        dictionary_to_add_to.setdefault(k, v)
