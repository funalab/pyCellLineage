"""
Author: Joel Nakatani
Overview:

Parameters:
"""

import scipy.signal as sp
from getIndependentLineage import getIndependentLineage
import pandas as pd
import numpy as np
import pandas as pd
from scipy import stats
import matplotlib.pyplot as plt
from tqdm import tqdm
import os


def write_Class(CellDF,target):
    counter = int(0)
    for lineage in getIndependentLineage(CellDF):
        lin_change = list()
        time_change = list()
        for cell_class in lineage['ATP_Class']:
            lin_change.append(cell_class)
        class_dict = {'ATP_Class':lin_change}
        df = pd.DataFrame(class_dict)
        df.to_csv(os.path.join(target,str(counter)+".csv"))
        counter = counter + 1

def hmm_prep(CellDF, save_dir, origin_frame=0):
    CellDF['ATP_Class'] = pd.np.nan
    avg_atp = sum(CellDF['ATP'])/len(CellDF['ATP'])
    class_list = list()
    for uid in range(origin_frame,len(CellDF['ATP'])):
        if float(CellDF['ATP'][uid]) <= avg_atp:
            class_list.append("low_atp")
        else:
            class_list.append("high_atp")
    CellDF['ATP_Class'] = class_list
    write_Class(CellDF,save_dir)
    return

if __name__ == "__main__":
    from annotateLineageIdx import annotateLineageIdx
    matFilePath = ('/Users/itabashi/Research/Analysis/Schnitzcells/'
                   '9999-99-99/488/data/488_lin.mat')
    segImgsPath = ('/Users/itabashi/Research/Analysis/Schnitzcells/'
                   '9999-99-99/488/segmentation/')
    rawImgsPath = ('/Users/itabashi/Research/Experiment/microscope/'
                   '2018/08/28/ECTC_8/Pos0/forAnalysis/488FS/')
    cellDfWPL = annotateLineageIdx(matFilePath, segImgsPath, rawImgsPath)
    cellDfWPL = cellular_ageTracking(cellDfWPL)

