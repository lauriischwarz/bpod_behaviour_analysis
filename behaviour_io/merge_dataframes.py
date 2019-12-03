
import pandas as pd
import pathlib


def merge(dfs):
    df_all = pd.DataFrame()
    for df in dfs:
        df_all = df.append(df)
    return df_all


root_folder = pathlib.Path('/Users/lauraschwarz/Documents/Bpod_raw/')
fpaths = root_folder.rglob('*_dataframe.csv')
dfs= [pd.read_csv(str(fpath)) for fpath in fpaths]
all_df = merge(dfs)
