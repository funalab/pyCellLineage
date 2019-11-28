import pandas as pd
"""
Author: Joel Nakatani
Overview:
Makes a shorter lineage from given time point and lineage
Parameters:
thr - time point where lineage will be cut
Df - dataframe created by pyLineage
"""


def short_lineage(Df,thr=3):
    Df = Df[Df['Z']<thr]
    for uid in Df[Df['Z'] == max(Df['Z'])]['uID']:
        Df.loc[uid,'daughter1ID'] = -1
        Df.loc[uid,'daughter2ID'] = -2
    for value in range(len(Df)):
        if value not in Df['uID'].unique():
            prevalue = value
            print "pre-"+str(value)
            while value not in Df['uID'].unique():
                value = value+1
            print "post-"+str(value)
            Df = Df.replace(to_replace=int(value),value=int(prevalue))
    Df = Df.reset_index(drop=True)
    return Df

if __name__ == "__main__":
    short_lineage(pd.read_csv("/Users/nakatani/workspace/jupyter/CSVs/2019_1016_Glc_rich/Rich_ATP.csv"),8)
