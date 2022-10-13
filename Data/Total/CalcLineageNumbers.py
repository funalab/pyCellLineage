"""
Author: Joel Nakatani
Overview:

Parameters:
"""

from pyCellLineage.lineageIO.annotateLineageIdx import annotateLineageIdx as annt
from pyCellLineage.PDAnalysis.calcRetro import RetrospectiveSampling as RS
from pyCellLineage.PDAnalysis.calcGEL import CalcGEL
import pyCellLineage as myPackage

import pandas as pd
import os
import argparse
import pickle
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import numpy as np
from scipy.stats import mannwhitneyu as npTtest
from scipy.stats import ttest_ind as tTest

if __name__ == "__main__":
    root = os.path.join(os.path.dirname(myPackage.__file__), 'Data')
    TotalDF = pd.DataFrame(columns=[
        'Average Number of Divisions', 'Growth Rate (1/h)', 'Average ATP (mM)',
        'Total Experimental Time (h)'
    ])
    condName = {'poor': 'deprived', 'rich': 'control'}

    for cond in ['poor', 'rich']:
        names = []

        for smpl in range(1, 4):
            target = os.path.join(root, f'glc_{cond}', f'sample{smpl}')
            fName = os.path.join(target, 'CellDf.csv')
            df = pd.read_csv(fName)
            indiLins = RS(df)
            divs = indiLins.countDivi(df)
            atps = df['intensity'].dropna()
            with open(os.path.join(target, f'GEL_{cond}_{smpl}.log')) as f:
                GR = float(f.read())
            name = f'glc_{condName[cond]} sample{smpl}'
            TotalDF.loc[name] = [
                sum(divs) / len(divs), GR,
                sum(atps) / len(atps),
                max(df['Z']) - min(df['Z']) + 1
            ]
            names.append(name)
            print(TotalDF)
        condDF = TotalDF.loc[names]
        condMean = condDF.mean()
        condVar = condDF.var()
        TotalDF.loc[f'{condName[cond]} Averages'] = condMean
        TotalDF.loc[f'{condName[cond]} Variances'] = condVar
    TotalDF.to_excel('./LineageDataNumbers.xlsx')
