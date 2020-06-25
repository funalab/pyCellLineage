"""
Author: Joel Nakatani
Overview:

Parameters:
"""

import matplotlib.pyplot as plt
import os
import numpy as np


def createHistMovie(CellDf,atpMax=None,freqMax=None,saveDir=None):
    for i in range(max(CellDf['Z'])):
        data = CellDf[CellDf['Z']==i]['ATP']
        print data.skew()
        fig = plt.figure()
        plt.hist(data.dropna())
            
        if atpMax != None:
            plt.xlim(0,atpMax)
        else:
            plt.xlim(0,max(CellDf['ATP'])+1)
        if freqMax != None:
            plt.ylim(0,freqMax)
        plt.title("t="+str(i)+"\n skewness="+str(data.skew()))
        if saveDir != None:
            if not os.path.isdir(savePath):
                os.mkdir(saveDir)
            fname = str(i)+".png"
            saveFile = os.path.join(saveDir,fname)
            fig.savefig(saveFile)
        plt.show()

#if __name__ == "__main__":
    
