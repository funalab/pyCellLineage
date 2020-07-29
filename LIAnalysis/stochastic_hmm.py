"""
Author: Joel Nakatani
Overview:
write_Class:
 writes CellDF 'target' class in csv files ordered in numbers by lineage.
 All csvs are created as '#.csv' with label ATP_Class.
 Parameters:
  CellDF: Cell Data Frame
  target: target of Data Frame (ATP_Class,Rand_Class)
  save_dir: save directory for created csvs.

hmm_prep:
 sorts ATP DF into high low classes.
 uses mean of lineage tree by default.
 writes to ATP_Class.
 Parameters:
  CellDF: Cell Data Frame
  save_dir: save directory if none write_class will not be used (default None)
  origin_frame: start of frames (default 0) 
  thr: threshold to separate ATP conc to two class if None the average of the whole tree will be used
  hname: name of Class expressing higher than thr (default None)
  lname: name of Class expressing lower than thr (default None)

hmm_randomize:
 randomize all ATP within lineage tree.
 writes to Rand_Class.
 Parameters:
  CellDF: Cell Data Frame
  save_dir: uses dir to save lineages using write_class creates random dir within given dir (default None)
  origin_frame: start of frames (default 0) 
"""

import scipy.signal as sp
from pyLineage.lineageIO.getIndependentLineage import getIndependentLineage
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
    avgList = None
    if hname == None:
        hname = "high_atp"
    if lname == None:
        lname = "low_atp"
    if thr == None:
        avgList = list()
        for i in range(origin_frame,max(CellDF['Z'])+1):
            timeframeATP = CellDF[CellDF['Z']==i]['ATP'].dropna()
            avgList.append(sum(timeframeATP)/len(timeframeATP))
    elif thr == 'All_avg':
        avg_atp = sum(CellDF['ATP'])/len(CellDF['ATP'])
    elif thr == 'Median':
        avg_atp = CellDF['ATP'].median()
    else:
        avg_atp = thr
    
    class_list = list()
    for uid in range(origin_frame,len(CellDF['ATP'])):
        if avgList != None:
            time = int(CellDF[CellDF['uID']==uid]['Z']) - origin_frame
            avg_atp = avgList[time]
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
        print("Make ATP_Class zone first")
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

def read_states(CellDF,read_dir):
    file_names = sorted(os.path.dirlist(read_dir))
    file_names = [x for x in file_names if "csv" in x]
    dict_fname = list(zip(list(range(len(file_names))),file_names))
    i = 0
    dict_states = dict()
    for lineage in getIndependentLineage(CellDF):
        hstates = list(pd.read_csv(dict_fname[i]))
        ids = list(lineage['fuID'])
        if len(hstates) == len(ids):
            dict_states.update(list(zip(ids,hstates)))
        else:
            print("Error")
            exit()
        i = i + 1
    all_states = list(dict_states.values())
    if len(all_states) == len(CellDF):
        CellDF["States"] = all_states
    else:
        CellDF["States"] = pd.np.nan
        print("Error in Total State size")
        exit()
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

