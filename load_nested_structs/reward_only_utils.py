
import numpy as np
import matplotlib.pylab as plt


def raster_reward_spikes(actual_trial_start_time, outcome_state_times, signals_spikes, unique_cluster_ids, cell_id):
    half_sec_before = outcome_state_times[:, 0] - 3
    one_sec_after = outcome_state_times[:, 0] + 3
    histogram_starts = half_sec_before
    histogram_ends = one_sec_after

    cell_idx = np.where(unique_cluster_ids == cell_id)[0]
    cell_idx = cell_idx[0]
    cell_spikes = signals_spikes[cell_idx]
    unitless_spike_times = np.asarray(cell_spikes)

    fig, ax = plt.subplots(1, 1, figsize=(30, 20))

    for trial_num, trial_start_time in enumerate(actual_trial_start_time):
        histogram_start = histogram_starts[trial_num]
        histogram_end = histogram_ends[trial_num]
        trial_outcome_state_times = outcome_state_times[trial_num, :]

        spikes_in_time_window_idx = np.intersect1d(np.where(unitless_spike_times >= histogram_start),
                                                   np.where(unitless_spike_times <= histogram_end))
        spikes_in_time_window = unitless_spike_times[spikes_in_time_window_idx]
        normalised_spikes_in_window = spikes_in_time_window - trial_outcome_state_times[0]

        yvals = np.ones(np.shape(normalised_spikes_in_window)) * trial_num
        ax.scatter(normalised_spikes_in_window, yvals, color='k', marker='|')

    reward_line = ax.axvline(0, color='r')

    plt.xlabel('Time from reward (s)', fontsize=20)
    plt.ylabel('Trial (cell ' + str(cell_id) + ')', fontsize=20)
    plt.xlim((-3, 3))

    plt.show()


def hist_reward_spikes(actual_trial_start_time, outcome_state_times, signals_spikes, unique_cluster_ids,
                       cell_id, ms_bin_size=1):
    # deals with binning stuff
    bin_size = ms_bin_size / 1000
    num_bins = int((3-(-3)) / bin_size)
    bin_ranges = np.linspace(-3, 3, num=num_bins)

    # sets the edges for the histogram
    half_sec_before = outcome_state_times[:, 0] - 3
    one_sec_after = outcome_state_times[:, 0] + 3
    histogram_starts = half_sec_before
    histogram_ends = one_sec_after

    # gets the spikes for the cell ID
    cell_idx = np.where(unique_cluster_ids == cell_id)[0]
    cell_idx = cell_idx[0]
    cell_spikes = signals_spikes[cell_idx]
    unitless_spike_times = np.asarray(cell_spikes)

    num_trials = np.shape(actual_trial_start_time)[0]
    binned_spikes = np.zeros([num_trials, num_bins])

    fig, ax = plt.subplots(1, 1, figsize=(10, 5))

    for trial_num, trial_start_time in enumerate(actual_trial_start_time):
        histogram_start = histogram_starts[trial_num]
        histogram_end = histogram_ends[trial_num]
        trial_outcome_state_times = outcome_state_times[trial_num, :]

        # finds the spikes
        spikes_in_time_window_idx = np.intersect1d(np.where(unitless_spike_times >= histogram_start),
                                                   np.where(unitless_spike_times <= histogram_end))
        spikes_in_time_window = unitless_spike_times[spikes_in_time_window_idx]
        normalised_spikes_in_window = spikes_in_time_window - trial_outcome_state_times[0]

        # bins the spikes
        binned_spikes[trial_num, 0:num_bins - 1] = np.histogram(normalised_spikes_in_window, bins=bin_ranges, density=False)[0]/bin_size

    psth_values = np.mean(binned_spikes, 0)
    ax.plot(bin_ranges, psth_values, color='k')
    reward_line = ax.axvline(0, color='r')

    plt.xlabel('Time from reward (s)', fontsize=20)
    plt.ylabel('Mean firing rate (Hz) (cell ' + str(cell_id) + ')', fontsize=20)
    plt.xlim((-3, 3))

    plt.show()


def raster_trial_type_spikes(trial_type_num, trial_types, open_ephys_trial_starts, trial_raw_events, signals_spikes,
                             unique_cluster_ids, cell_id):

        # gets the trials of the correct type
        trials_of_that_type_id = np.where(trial_types == trial_type_num)
        trial_type_raw_events = trial_raw_events[trials_of_that_type_id]
        trial_type_oephys_TTLs = open_ephys_trial_starts[trials_of_that_type_id]

        # finds spikes for the cell you want
        cell_idx = np.where(unique_cluster_ids == cell_id)[0]
        cell_idx = cell_idx[0]
        cell_spikes = signals_spikes[cell_idx]
        unitless_spike_times = np.asarray(cell_spikes)

        # pre-allocates arrays for the trial timing events
        num_trials = np.shape(trial_type_raw_events)[0]
        trial_starts = np.zeros((num_trials, 2))
        outcome_state_times = np.zeros((num_trials, 2))
        actual_trial_start_time = np.zeros(num_trials)

        # sets fig params
        fig_height = max(num_trials/10, 2.2)
        fig, ax = plt.subplots(1, 1, figsize=(30, fig_height))

        for trial_num, trial in enumerate(trial_type_raw_events):
            actual_trial_start_time[trial_num] = trial_type_oephys_TTLs[trial_num]
            trial_starts[trial_num, :] = trial['States']['TaskStart']
            outcome_state_times[trial_num, :] = trial['States']['Outcome'] + actual_trial_start_time[trial_num]
            histogram_start = outcome_state_times[trial_num, 0] - 3
            histogram_end = outcome_state_times[trial_num, 0] + 3
            spikes_in_time_window_idx = np.intersect1d(np.where(unitless_spike_times >= histogram_start),
                                                       np.where(unitless_spike_times <= histogram_end))
            spikes_in_time_window = unitless_spike_times[spikes_in_time_window_idx]
            normalised_spikes_in_window = spikes_in_time_window - outcome_state_times[trial_num, 0]
            yvals = np.ones(np.shape(normalised_spikes_in_window)) * trial_num
            ax.scatter(normalised_spikes_in_window, yvals, color='k', marker='|')

        reward_line = ax.axvline(0, color='r')

        plt.xlabel('Time from reward (s)', fontsize=20)
        plt.ylabel('Trial (cell ' + str(cell_id) + ')', fontsize=20)
        plt.xlim((-3, 3))

        plt.show()


def hist_trial_type_spikes(trial_type_num, trial_types, open_ephys_trial_starts, trial_raw_events, signals_spikes,
                           unique_cluster_ids, cell_id, ms_bin_size=1):

    # gets the trials of the correct type
    trials_of_that_type_id = np.where(trial_types == trial_type_num)
    trial_type_raw_events = trial_raw_events[trials_of_that_type_id]
    trial_type_oephys_TTLs = open_ephys_trial_starts[trials_of_that_type_id]

    # deals with binning stuff
    bin_size = ms_bin_size / 1000
    num_bins = int((3-(-3)) / bin_size)
    bin_ranges = np.linspace(-3, 3, num=num_bins)

    # gets the spikes for the cell you want
    cell_idx = np.where(unique_cluster_ids == cell_id)[0]
    cell_idx = cell_idx[0]
    cell_spikes = signals_spikes[cell_idx]
    unitless_spike_times = np.asarray(cell_spikes)

    # pre-allocates arrays
    num_trials = np.shape(trial_type_raw_events)[0]
    binned_spikes = np.zeros([num_trials, num_bins])
    trial_starts = np.zeros((num_trials, 2))
    outcome_state_times = np.zeros((num_trials, 2))
    actual_trial_start_time = np.zeros(num_trials)

    fig, ax = plt.subplots(1, 1, figsize=(10, 5))

    for trial_num, trial in enumerate(trial_type_raw_events):
        actual_trial_start_time[trial_num] = trial_type_oephys_TTLs[trial_num]
        trial_starts[trial_num, :] = trial['States']['TaskStart']
        outcome_state_times[trial_num, :] = trial['States']['Outcome'] + actual_trial_start_time[trial_num]
        histogram_start = outcome_state_times[trial_num, 0] - 3
        histogram_end = outcome_state_times[trial_num, 0] + 3
        spikes_in_time_window_idx = np.intersect1d(np.where(unitless_spike_times >= histogram_start),
                                                   np.where(unitless_spike_times <= histogram_end))
        spikes_in_time_window = unitless_spike_times[spikes_in_time_window_idx]
        normalised_spikes_in_window = spikes_in_time_window - outcome_state_times[trial_num, 0]

        # bins the spikes
        binned_spikes[trial_num, 0:num_bins - 1] = np.histogram(normalised_spikes_in_window, bins=bin_ranges, density=False)[0]/bin_size

    psth_values = np.mean(binned_spikes, 0)
    ax.plot(bin_ranges, psth_values, color='k')
    reward_line = ax.axvline(0, color='r')

    plt.xlabel('Time from reward (s)', fontsize=20)
    plt.ylabel('Mean firing rate (Hz) (cell ' + str(cell_id) + ')', fontsize=20)
    plt.xlim((-3, 3))

    plt.show()


def raster_reward_licks(actual_trial_start_time, outcome_state_times, lick_times):
    half_sec_before = outcome_state_times[:, 0] - 3
    three_secs_after = outcome_state_times[:, 0] + 3
    histogram_starts = half_sec_before
    histogram_ends = three_secs_after

    fig, ax = plt.subplots(1, 1, figsize=(10, 5))

    for trial_num, trial_start_time in enumerate(actual_trial_start_time):
        histogram_start = histogram_starts[trial_num]
        histogram_end = histogram_ends[trial_num]
        trial_outcome_state_times = outcome_state_times[trial_num, :]
        trial_licks = lick_times[trial_num]
        
        if np.any(trial_licks != None):
            licks_in_time_window_idx = np.intersect1d(np.where(trial_licks >= histogram_start),
                                                   np.where(trial_licks <= histogram_end))
           
            if licks_in_time_window_idx != []:
                licks_in_time_window = trial_licks[licks_in_time_window_idx]
                normalised_licks_in_window = licks_in_time_window - trial_outcome_state_times[0]

                yvals = np.ones(np.shape(normalised_licks_in_window)) * trial_num
                ax.scatter(normalised_licks_in_window, yvals, color='r', marker='|')

    reward_line = ax.axvline(0, color='r')

    plt.xlabel('Time from reward (s)', fontsize=20)
    plt.ylabel('Trial', fontsize=20)
    plt.xlim((-3, 3))

    plt.show()
    return()

