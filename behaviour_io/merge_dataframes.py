
import pandas as pd
import pathlib

from behaviour_io.constants import ROOT_FOLDER


def merge_dataframes(dfs):
    df_all = pd.DataFrame()
    for df in dfs:
        df_all = df.append(df)
    return df_all


root_folder = pathlib.Path(ROOT_FOLDER)
fpaths = root_folder.rglob('*_dataframe.csv')
dfs = [pd.read_csv(str(fpath)) for fpath in fpaths]
all_df = merge_dataframes(dfs)


