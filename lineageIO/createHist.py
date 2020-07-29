"""
Author: Joel Nakatani
Overview:

Parameters:
"""

import matplotlib.pyplot as plt
import os
import numpy as np
from scipy.stats import skew

def bootstrap(data,itr=10000):
    data = data.dropna()
    orgSkew = data.skew()
    mean = float(data.mean())
    std = float(data.std())
    leng = len(data)
    skewList = list()
    for i in range(itr):
        #print mean,std,leng
        tmpData = np.random.normal(mean,std,leng)
        skewList.append(skew(tmpData))

    p = sum(i > orgSkew for i in skewList)/float(itr)
    return p

def createHist(CellDf,atpMax=None,freqMax=None,saveDir=None,fname=None,minCells=100):
    data = CellDf['ATP']
    fig = plt.figure()
    plt.hist(data.dropna())
    # plot parameters
    if atpMax != None:
        plt.xlim(0,atpMax)
    else:
        plt.xlim(0,max(CellDf['ATP'])+1)
        
    if freqMax != None:
            plt.ylim(0,freqMax)

    # plot depending on samples
    if len(data) > minCells:
        plt.title("t="+str(i)+"\n skewness="+str(data.skew())+"(p="+str(bootstrap(data))+")")
    else:
        plt.title("t="+str(i)+"\n skewness="+str(data.skew()))
    if saveDir != None:
        if not os.path.isdir(savePath):
            os.mkdir(saveDir)
        if fname == None:
            fname = "Hist.png"
        saveFile = os.path.join(saveDir,fname)
        fig.savefig(saveFile)
    plt.show()
    return

def createHistMovie(CellDf,atpMax=None,freqMax=None,saveDir=None,minCells=100):
    for i in range(max(CellDf['Z'])):
        if saveDir != None:
            if not os.path.isdir(savePath):
                os.mkdir(saveDir)
            fname = str(i)+".png"
        createHist(CellDf[CellDf['Z']==i],atpMax=atpMax,freqMax=freqMax,saveDir=saveDir,fname=fname,minCells=minCells)
    return

#if __name__ == "__main__":
    
