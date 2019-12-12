
import pandas as pd
import pathlib

from behaviour_io.constants import ROOT_FOLDER, BPOD_PROTOCOL


def merge_dataframes(dfs):  #issue: append does not append to existing df but only chucks in the current df
    df_all = pd.concat([df for df in dfs], ignore_index=True, sort=True)
    return df_all


root_folder = pathlib.Path(ROOT_FOLDER)
fpaths = root_folder.rglob('*_dataframe.csv')
dfs = [pd.read_csv(str(fpath)) for fpath in fpaths]
all_df = merge_dataframes(dfs)
bpod_protocol = BPOD_PROTOCOL

output_dir = f'{ROOT_FOLDER}{bpod_protocol}Data_Analysis/'
pathlib.Path(output_dir).mkdir(parents=True, exist_ok=True)
all_df.to_csv(f"{output_dir}_merged_dataframe.csv")

print(all_df.AnimalID)
