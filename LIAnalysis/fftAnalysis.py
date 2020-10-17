#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# -*- coding: utf-8 -*-
#
# Last modified: Mon, 28 Jan 2019 14:31:47 +0900
import numpy as np
import os
import pandas as pd
from pyLineage.lineageIO.getIndependentLineage import getIndependentLineage
import scipy.signal as sp
from scipy import stats
import matplotlib.pyplot as plt
from tqdm import tqdm

def write_ATPChange(CellDF,save_dir):
    counter = int(0)
    if not os.path.isdir(save_dir):
        os.mkdir(save_dir)
    for lineage in getIndependentLineage(CellDF):
        lin_change = list()
        time_change = list()
        
        for cell_id in lineage['uID']:
            cell = CellDF[CellDF['uID'] == cell_id]
            lin_change.append(float(cell['ATP']))
            time_change.append(int(cell['Z']))
        dict = {'time':time_change,'atp':lin_change}
        df = pd.DataFrame(dict)
        df.to_csv(os.path.join(save_dir,str(counter)+".csv"))
        counter = counter + 1
        return

    
def plot_IndiLine(csvPath,saveDir=None,ylim=10,xlim=None,pltshow=None):
    plt.cla()
    plt.clf()
    GPR_chg = pd.read_csv(csvPath, header=1)
    GPR_chg = GPR_chg.T[1:]
    GPR_chg.index = GPR_chg.index.astype(np.float64)
    atpChange = GPR_chg
    for i in tqdm(range(len(atpChange.columns))):
        if len(atpChange[i].unique()) > len(atpChange[i])/2:
            plt.plot(atpChange.index, atpChange[i])
            plt.xlabel('time (hours)')
            plt.ylabel('[ATP] (mM)')
            plt.tight_layout()
            plt.ylim((0,ylim))
            plt.xlim((0,xlim))
    if saveDir != None:
        plt.savefig(os.path.join(saveDir,"indi.png"))
    if pltshow != None:
        plt.show()
    plot_frequency(atpChange,saveDir=saveDir)
    return

def plot_frequency(atpChange,saveDir=None,pltshow=None):
    maxAmp = list()
    maxFreq = list()
    dt = float(atpChange.index[-1]) / 1000
    for i in range(len(atpChange.columns)):
        t = atpChange.index
        f = np.array(atpChange[i])
        F = np.fft.fft(f)
        Amp = np.abs(F)
        freq = np.linspace(0, 1.0/dt, len(atpChange[i]))
        plt.plot(freq, Amp)
        plt.xlabel('Frequency')
        plt.ylabel('|F(k)|')
        maxAmp.append(np.max(Amp[1:len(t)/2]))
        index = np.where(Amp[2:len(t)/2] == np.max(Amp[2:len(t)/2]))
        maxFreq.append(freq[index[0][0] + 1])
    if saveDir != None:
        plt.savefig(os.path.join(saveDir,"freq.png"))
    if pltshow != None:
        plt.show()
    plot_atpAmp(atpChange,maxAmp,saveDir=saveDir)
    plot_atpFreq(atpChange,maxFreq, saveDir=saveDir)
    return

def plot_atpAmp(atpChange,maxAmp,saveDir=None,ylim=8):
    lastATP = [atpChange[i].values[-1] for i in range(len(atpChange.columns))]
    plt.scatter(maxAmp, lastATP)
    plt.xlabel('maximum Amplitude')
    plt.ylabel('[ATP]')
    plt.ylim((0,ylim))
    pc = np.polyfit(x = maxAmp, y = lastATP, deg = 1)
    r, p = stats.spearmanr(maxAmp, lastATP)
    print('r : ', r)
    print('p : ', p)
    print(pc)
    if saveDir != None:
        plt.savefig(os.path.join(saveDir,"atpAmp.png"))
    plt.show()
    return
        
def plot_atpFreq(atpChange, maxFreq, saveDir=None, ylim=8):
    lastATP = [atpChange[i].values[-1] for i in range(len(atpChange.columns)) ]
    plt.scatter(maxFreq, lastATP)
    plt.xlabel('maximum Frequency ($h^{-1}$)')
    plt.ylabel('[ATP]')
    plt.ylim((0,ylim))
    r, p = stats.spearmanr(maxFreq, lastATP)
    print('r : ', r)
    print('p : ', p)
    plt.title("R = " + str(r))
    if saveDir != None:
        plt.savefig(os.path.join(saveDir,"atpFreq.png"))
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
