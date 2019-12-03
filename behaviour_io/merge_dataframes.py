import os
import sys
sys.path.append("../") # go to parent
import pandas as pd
import warnings

warnings.filterwarnings('ignore')


def merge_DF(AnimalID_list):
    # output a list of animals ready to pull
    # Task
    BpodProtocol = '/Two_Alternative_Choice/'
    # Behavioural data
    general_directory = '/Users/lauraschwarz/Documents/Bpod_raw/'

    for AnimalID in os.listdir(general_directory):
        df_file_path = general_directory + AnimalID + BpodProtocol + 'Data_Analysis/' + AnimalID + '_dataframe.csv'
        if os.path.exists(df_file_path):
            print('Found data for ' + AnimalID)

    data_frames = []
    # Read the dataframes and merge them
    for AnimalID in AnimalID_list:
        df_file_path = f"{general_directory}{AnimalID}{BpodProtocol}Data_Analysis/{AnimalID}_dataframe.csv"
        animal_df = pd.read_pickle(df_file_path)
        data_frames.append(animal_df)
    animals_df = pd.concat(data_frames, ignore_index=True)

    # Create out directory if it does not exist
    output_dir = general_directory + '-'.join(AnimalID_list) + '_Analysis/'
    if not os.path.isdir(output_dir):
        os.mkdir(output_dir)

    return animals_df
