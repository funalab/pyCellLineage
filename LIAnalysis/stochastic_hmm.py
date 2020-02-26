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


def write_Class(CellDF,target,save_dir):
    counter = int(0)
    if not os.path.isdir(save_dir):
        os.mkdir(save_dir)
    for lineage in getIndependentLineage(CellDF):
        lin_change = list()
        time_change = list()
        for cell_class in lineage[target]:
            lin_change.append(cell_class)
        class_dict = {'ATP_Class':lin_change}
        df = pd.DataFrame(class_dict)
        df.to_csv(os.path.join(save_dir,str(counter)+".csv"))
        counter = counter + 1

def hmm_prep(CellDF, save_dir=None, origin_frame=0, thr=None, hname=None,lname=None):
    CellDF['ATP_Class'] = pd.np.nan
    if hname == None:
        hname = "high_atp"
    if lname == None:
        lname = "low_atp"
    if thr == None:
        avg_atp = sum(CellDF['ATP'])/len(CellDF['ATP'])
    else:
        avg_atp = thr
        
    class_list = list()
    for uid in range(origin_frame,len(CellDF['ATP'])):
        if float(CellDF['ATP'][uid]) <= avg_atp:
            class_list.append(lname)
        else:
            class_list.append(hname)
    CellDF['ATP_Class'] = class_list
    if save_dir != None:
        write_Class(CellDF,'ATP_Class',save_dir)
    return CellDF

def hmm_randomize(CellDF, save_dir=None, origin_frame=0):
    CellDF['Rand_Class'] = pd.np.nan
    if len(CellDF['ATP_Class']) == 0:
        print "Make ATP_Class zone first"
        exit()
    else:
        lin_len = len(CellDF)
        origin_class = list(CellDF['ATP_Class'])
        rand_class = list(np.random.choice(origin_class,size=lin_len,replace=False))
        CellDF['Rand_Class'] = rand_class
    if save_dir != None:
        save_dir = os.path.join(save_dir,"random")
        write_Class(CellDF,'Rand_Class',save_dir)
#        for lineage in getIndependentLineage(CellDF):
#            lin_len = len(lineage)
#            origin_class = lineage['ATP_Class']
#            rand_class = list(np.random.choice(origin_class,size=lin_len,replace=False))
#            lineage['Rand_Class'] = rand_class
    return CellDF


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

