"""
Author: Joel Nakatani
Overview:
makeHistFromRawImage(matImgsPath,rawImgsPath,savePath=None)
 makes hist from given rawImgsPath and matImgsPath. uses rawimage and matlab segmentation

createHist(CellDf=None,data=None,atpMax=None,freqMax=None,saveDir=None,fname=None,z=None,minCells=100)
make Hist from data list or CellDf.
You can set atpMax,freqMax,saveDir and filename.
Also by giving a Z it would be included in the title.
minCells are set to 100. If less than that Hist will not be created.

createHistMovie(CellDf,atpMax=None,freqMax=None,saveDir=None,minCells=50)
makes movie from one CellDf using time frame.
each hist represents one time frame. parms are the same as above.

Parameters:
"""

import matplotlib.pyplot as plt
import os
import numpy as np
import pandas as pd
from scipy.stats import skew
from pyLineage.lineageIO.bootstrap import bootstrap
from pyLineage.lineageIO.extractIntensity import extractIntensity
from pyLineage.lineageIO.loadRawImgs import loadRawImgs
from pyLineage.lineageIO.loadMatImgs import loadMatImgs


def makeHistFromRawImage(matImgsPath,rawImgsPath,timelapse=False,savePath=None,minInten=0.,atpInten=None):
    segImgsList = loadMatImgs(matImgsPath)
    rawImgsList = loadRawImgs(rawImgsPath)
    intensityList = list()
    for frameIdx in range(0,len(segImgsList)):
        cellIndices = np.unique(segImgsList[frameIdx])
        cellIndices = np.delete(cellIndices,0)
        intensityList.append(extractIntensity(segImgsList[frameIdx],rawImgsList[frameIdx]))
    
    allIntens = list()
    if timelapse:
        atpMax=max(intensityList)
        count = 0
    for intens in intensityList:
        if timelapse:
            count += 1
            createHist(data=[i for i in intens if i > minInten],atpMax=atpMax,fname="Hist"+str(count)+".png",saveDir=savePath)
        allIntens = allIntens + list(intens.values())
    createHist(data=[i for i in allIntens if i > minInten],saveDir=savePath,atpMax=atpInten)

    
def createHist(CellDf=None,data=None,atpMax=None,freqMax=None,saveDir=None,fname=None,z=None,minCells=50):
    if CellDf is not None:
        data = CellDf['ATP']
    else:
        if data is not None and type(data) is list:
            data = pd.Series(data)
        else:
            print("Error: input data(frame) in createHist")
            exit(-1)
    fig = plt.figure()
    plt.hist(data.dropna(),bins=20)
    # plot parameters
    if atpMax != None:
        plt.xlim(0,atpMax)
    else:
        plt.xlim(0,max(data)+1)
        
    if freqMax != None:
            plt.ylim(0,freqMax)

    # plot depending on samples
    if z != None:
        titleName = "t="+str(z)
    else:
        titleName = "Histogram"

    titleName = titleName + "\n skewness="+str(data.skew())
    
    if len(data) > minCells:
        plt.title(titleName+"(p="+str(bootstrap(data))+")")
    else:
        plt.title(titleName)
    
    if saveDir != None:
        if not os.path.isdir(saveDir):
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
            if not os.path.isdir(saveDir):
                os.mkdir(saveDir)
            fname = str(i)+".png"
        createHist(CellDf[CellDf['Z']==i],atpMax=atpMax,freqMax=freqMax,saveDir=saveDir,fname=fname,z=i,minCells=minCells)
    return

#if __name__ == "__main__":
if __name__ == "__main__":
    from .annotateLineageIdx import annotateLineageIdx
    matFilePath = ('/Users/itabashi/Research/Analysis/Schnitzcells/'
                   '9999-99-99/488/data/488_lin.mat')
    segImgsPath = ('/Users/itabashi/Research/Analysis/Schnitzcells/'
                   '9999-99-99/488/segmentation/')
    rawImgsPath = ('/Users/itabashi/Research/Experiment/microscope/'
                   '2018/08/28/ECTC_8/Pos0/forAnalysis/488FS/')
    cellDfWPL = annotateLineageIdx(matFilePath, segImgsPath, rawImgsPath)
    createHist(cellDfWPL)
    
