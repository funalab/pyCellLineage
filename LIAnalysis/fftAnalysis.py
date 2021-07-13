#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# -*- coding: utf-8 -*-
#
# Last modified: Mon, 28 Jan 2019 14:31:47 +0900
import numpy as np
import os
import pandas as pd
from ..lineageIO.getIndependentLineage import getIndependentLineage
import scipy.signal as sp
from scipy import stats
import matplotlib.pyplot as plt
import statistics

from ..util.isNotebook import isnotebook
if isnotebook():
    from tqdm.notebook import tqdm
else:
    from tqdm import tqdm

def write_ATPChange(CellDF,save_dir,attr='intensity',changedCSVpath=None):
    counter = int(0)
    skiptList = list()
    if changedCSVpath != None:
        if os.path.exists(changedCSVpath):
            skipt = pd.read_csv(changedCSVpath)
            skiptList = list(skipt[skipt['change']=='-']['frame'])
            
    if not os.path.isdir(save_dir):
        os.mkdir(save_dir)
    for lineage in getIndependentLineage(CellDF):
        lin_change = list()
        time_change = list()
        
        for cell_id in lineage['uID']:
            cell = CellDF[CellDF['uID'] == cell_id]
            if int(cell['Z']) not in skiptList:
                lin_change.append(float(cell[attr]))
                time_change.append(int(cell['Z']))
        dict = {'time':time_change,'atp':lin_change}
        df = pd.DataFrame(dict)
        df.to_csv(os.path.join(save_dir,str(counter)+".csv"))
        counter = counter + 1
    return

    
def plot_IndiLine(csvPath,saveDir=None,ylim=14,xlim=None,pltshow=False):
    plt.cla()
    plt.clf()
    GPR_chg = pd.read_csv(csvPath, header=1)
    GPR_chg = GPR_chg.T[1:]
    GPR_chg.index = GPR_chg.index.astype(np.float64)
    atpChange = GPR_chg
    for i in tqdm(list(range(len(atpChange.columns)))):
        if len(atpChange[i].unique()) > len(atpChange[i])/2:
            plt.plot(range(len(atpChange)), atpChange[i])
            plt.xlabel('time (hours)')
            plt.ylabel('[ATP] (mM)')
            plt.tight_layout()
            plt.ylim((0,ylim))
            plt.xlim((0,xlim))
    if saveDir != None:
        plt.savefig(os.path.join(saveDir,"indi.pdf"))
    if pltshow:
        plt.show()
    plot_frequency(atpChange,saveDir=saveDir)
    return

def plot_frequency(atpChange,saveDir=None,pltshow=False):
    maxAmp = list()
    maxFreq = list()
    dt = float(atpChange.index[-1]) / 1000
    for i in range(len(atpChange.columns)):
        t = atpChange.index
        f = np.array(atpChange[i])
        F = np.fft.fft(f)
        Amp = np.abs(F)
        freq = np.linspace(0, 1.0/dt, len(atpChange[i]))
        plt.cla()
        plt.clf()
        plt.plot(freq, Amp)
        plt.xlabel('Frequency')
        plt.ylabel('|F(k)|')
        maxAmp.append(np.max(Amp[1:int(len(t)/2)]))
        index = np.where(Amp[2:int(len(t)/2)] == np.max(Amp[2:int(len(t)/2)]))
        maxFreq.append(freq[index[0][0] + 1])
    if saveDir != None:
        plt.savefig(os.path.join(saveDir,"freq.pdf"))
    if pltshow:
        plt.show()
    plot_atpAmp(atpChange,maxAmp,saveDir=saveDir)
    plot_atpFreq(atpChange,maxFreq, saveDir=saveDir)
    plot_AmpFreq(maxAmp,maxFreq, saveDir=saveDir)
    return

def plot_atpAmp(atpChange,maxAmp,saveDir=None,ylim=8,xlim=25,pltshow=False,mode='last'):
    plt.cla()
    plt.clf()
    medATP = [statistics.median(atpChange[i]) for i in range(len(atpChange.columns)) ]
    lastATP = [atpChange[i].values[-1] for i in range(len(atpChange.columns))]
    maxATP = [max(atpChange[i]) for i in range(len(atpChange.columns)) ]
    minATP = [min(atpChange[i]) for i in range(len(atpChange.columns)) ]
        
    if mode == 'median':
        ATP = medATP
    elif mode == 'last':
        ATP = lastATP
    elif mode == 'max':
        ATP = maxATP
    elif mode == 'min':
        ATP = minATP
    else:
        sys.exit(-1)

    plt.scatter(maxAmp, ATP)
    plt.xlabel('maximum Amplitude')
    plt.ylabel('[ATP]')
    plt.ylim((0,ylim))
    plt.xlim((0,xlim))
    pc = np.polyfit(x = maxAmp, y = ATP, deg = 1)
    r, p = stats.spearmanr(maxAmp, ATP)
    print(('r : ', r))
    print(('p : ', p))
    print(pc)
    if saveDir != None:
        plt.savefig(os.path.join(saveDir,mode+"atpAmp.pdf"))
        data = {'maxAmp':maxAmp,'medianATP':medATP,'maxATP':maxATP,'minATP':minATP,'lastATP':lastATP}
        DF = pd.DataFrame(data=data,columns=data.keys())
        DF.to_csv(os.path.join(saveDir,"atpAmp.csv"))        
    if pltshow:
        plt.show()
    return
        
def plot_atpFreq(atpChange, maxFreq, saveDir=None, ylim=8,xlim=25,pltshow=False,mode='last'):
    plt.cla()
    plt.clf()
    medATP = [statistics.median(atpChange[i]) for i in range(len(atpChange.columns)) ]
    lastATP = [atpChange[i].values[-1] for i in range(len(atpChange.columns)) ]
    maxATP = [max(atpChange[i]) for i in range(len(atpChange.columns)) ]
    minATP = [min(atpChange[i]) for i in range(len(atpChange.columns)) ]
        
    if mode == 'median':
        ATP = medATP
    elif mode == 'last':
        ATP = lastATP
    elif mode == 'max':
        ATP = maxATP
    elif mode == 'min':
        ATP = minATP
    else:
        sys.exit(-1)    
    plt.scatter(maxFreq, ATP)
    plt.xlabel('maximum Frequency ($h^{-1}$)')
    plt.ylabel('[ATP]')
    plt.ylim((0,ylim))
    plt.xlim((0,xlim))
    r, p = stats.spearmanr(maxFreq, ATP)
    print('r : ', r)
    print('p : ', p)
    plt.title("R = " + str(r))
    if saveDir != None:
        plt.savefig(os.path.join(saveDir,mode+"atpFreq.pdf"))
        data = {'maxFreq':maxFreq,'medianATP':medATP,'maxATP':maxATP,'minATP':minATP,'lastATP':lastATP}
        DF = pd.DataFrame(data=data,columns=data.keys())
        DF.to_csv(os.path.join(saveDir,"atpFreq.csv"))
    if pltshow:
        plt.show()
    return

def plot_AmpFreq(maxAmp,maxFreq,saveDir=None,ylim=8,xlim=25,pltshow=False,mode='last'):
    plt.cla()
    plt.clf()
    plt.scatter(maxAmp, maxFreq)
    plt.xlabel('maximum Amplitude')
    plt.ylabel('maximum Freq')
    plt.ylim((0,ylim))
    plt.xlim((0,xlim))
    r, p = stats.spearmanr(maxAmp, maxFreq)
    print(('r : ', r))
    print(('p : ', p))
    if saveDir != None:
        plt.savefig(os.path.join(saveDir,mode+"AmpFreq.pdf"))
    if pltshow:
        plt.show()
    return


def fftAnalysis(cellDfWPL):
    '''
    Analysis all lineages with Fast Fourier Transform.

    Parameters
    ----------
    cellDfWPL

    Returns
    -------
    '''



if __name__ == "__main__":
    main()
