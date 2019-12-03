import load_nested_structs as load_ns
import sys
from behaviour_io.get_data_funcs import get_settings, convert_raw_events_to_dictionaries

sys.path.append("../") # go to parent
import glob
import ntpath
import numpy as np
import warnings

warnings.filterwarnings('ignore')


def ReadAnimalData(GeneralDirectory, AnimalID, BpodProtocol, printout=True):
    # Reads all data from one animal and one protocol

    # Initialize return lists
    ExperimentFiles = []  # to store experiment names
    ExperimentData = []  # to store the dictionaries
    ntrialsDistribution = []  # to visualize the distribution of the number of trials
    Protocols = []  # store the protocols
    Stimulations = []  # store the stimulated protocols
    Muscimol = []  # store information about the muscimol
    counter = 0
    mat_file_path = f"{GeneralDirectory}{AnimalID}{BpodProtocol}Session Data/*.mat"
    filelist = glob.glob(mat_file_path)
    filelist.sort()

    for file_path in filelist:
        data = load_ns.loadmat(file_path)

        if not "nTrials" in data["SessionData"]:
            continue

        if "SessionData" in data:
            ntrials = data["SessionData"]["nTrials"]

        ExperimentFiles.append(file_path)

        parse_trial_settings(Muscimol,
                             Protocols,
                             Stimulations,
                             counter,
                             data,
                             file_path,
                             ntrials,
                             ntrialsDistribution,
                             printout)

        # as RawEvents.Trial is a cell array of structs in MATLAB,
        # we have to loop through the array and convert the structs to dicts

        trial_raw_events = data["SessionData"]["RawEvents"]["Trial"]
        try:
            trial_raw_events = convert_raw_events_to_dictionaries(trial_raw_events)
        except Exception as e:
            print(e)
            trial_raw_events = None

        if trial_raw_events is not None:
            data["SessionData"]["RawEvents"]["Trial"] = trial_raw_events
        else:
            data["SessionData"]["RawEvents"]["Trial"] = np.nan

        # Save the data in a list
        ExperimentData.append(data)
        counter += 1

    return (
        ExperimentFiles,
        ExperimentData,
        ntrialsDistribution,
        Protocols,
        Stimulations,
        Muscimol,
    )


def parse_trial_settings(Muscimol, Protocols, Stimulations, counter, data, file_path, ntrials, ntrialsDistribution,
                         printout):
    # Parse the settings of the trials
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
            "{}: {}, {} trials on {}, stim {}, muscimol {}".format(
                counter,
                ntpath.basename(file_path),
                ntrials,
                protocol,
                stimulation,
                muscimol,
            )
        )
    ntrialsDistribution.append(ntrials)
    Protocols.append(protocol)
    Stimulations.append(stimulation)
    Muscimol.append(muscimol)

