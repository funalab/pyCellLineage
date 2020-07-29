#!/usr/bin/env python
# coding: utf-8

# In[1]:
from pyLineage.lineageIO.measurePhenotypes import measurePhenotypes
from pyLineage.lineageIO.create3DLineage import create3DLineage
from pyLineage.lineageIO.create2DLineage import create2DLineage
from pyLineage.LIAnalysis.stochastic_hmm import hmm_prep
from pyLineage.lineageIO.getIndependentLineage import getIndependentLineage
from pyLineage.LIAnalysis.fftAnalysis import write_ATPChange
from pyLineage.LIAnalysis.cellular_ageTracking import cellular_ageTracking
from pyLineage.lineageIO.createHist import createHistMovie
from pyLineage.lineageIO.createHist import createHist
from pyLineage.LIAnalysis.cellular_ageTracking import drawAgeFig
from pyLineage.LIAnalysis.fftAnalysis import plot_IndiLine
from pyLineage.lineageIO.lineage_editor import lineage_editor
from pyLineage.Analysis_Gui.Final_Analysis_GUI_Class import ModeScreens
from pyLineage.Analysis_Gui.modeIO import modeIO
from pyLineage.Analysis_Gui.path_prep import path_prep ## Works only for a specific directory structure(check examples)


import os
import pandas as pd
import sys



# Magic Numbers
atpMax = 10
genMax = 35
debug = False

def Total_ATP(cellDFWP,cond,num):
    totalDF = cellDFWP
    samples[cond][num] = False
    for cond in conditions:
        for num in sampleNum:
            if samples[cond][num]:
                paths = path_prep(samplePath[cond][num])
                CellDF = measurePhenotypes(paths['matFilePath'], paths['segImgsPath'], paths['rawImgsPath'])        
                totalDF = pd.concat([totalDF,CellDF])
    return totalDF


def Analysis_all(path,cond,num,mode,atpMax=None,genMax=None):
    hmmCellDF = None
    paths = path_prep(path)
    cellDFWP = measurePhenotypes(paths['matFilePath'], paths['segImgsPath'], paths['rawImgsPath'])        
    #parent of path
    saveDir = str('/'.join(os.path.abspath(path).split('/')[0:-1-0]))

    #Make Hist    
    if mode['Analysis']['hist']['normal']:
        saveDir_hist = os.path.join(saveDir,'Hist/')
        createHistMovie(cellDFWP,atpMax=atpMax,saveDir=saveDir_hist)
    elif mode['Analysis']['hist']['totalATP']:
        totalDF = Total_ATP(cellDFWP,cond,num)
        saveDir_hist = os.path.join(saveDir,'totalATP_Hist/')
        createHist(totalDF,atpMax=atpMax,saveDir=saveDir_hist)
        sys.exit(0)
    
    #make lineage
    if mode['lineage']['save']:
        savePathLin = os.path.join(saveDir,"lineage.pdf")
        create2DLineage(cellDFWP,attr='ATP',attrMax=atpMax, ylim=genMax,savePath=savePathLin)
    elif mode['lineage']['show']:
        create2DLineage(cellDFWP,attr='ATP',attrMax=atpMax, ylim=genMax)
    elif mode['lineage']['3d']:
        saveDir_3d = os.path.join(saveDir,'3dLin')
        create3DLineage(lineage_editor(None,None,None,DF=cellDFWP,mode=1),
                        attr='ATP',
                        attrMax=atpMax-1,
                        savePath=saveDir_3d)
    else:
        create2DLineage(cellDFWP,attr='ATP',attrMax=atpMax, ylim=genMax,show=False)
    #prepHmm
    if mode['Analysis']['hmmPrep']['mean']:
        saveDir_Indi = os.path.join(saveDir, 'IndiCell/')
        cellDFWP = hmm_prep(cellDFWP,save_dir=saveDir_Indi,lname="low",hname="high")        
    elif mode['Analysis']['hmmPrep']['median']:
        saveDir_Indi = os.path.join(saveDir, 'IndiCellMedian/')
        cellDFWP = hmm_prep(cellDFWP,thr='median',save_dir=saveDir_Indi,lname="low",hname="high")
        
    if mode['Analysis']['hmmPrep']['class']['2d']:
        saveDir_2dClass = os.path.join(saveDir,'Class_2dLin.pdf')
        hmmCellDF = hmm_prep(cellDFWP,lname=1,hname=2)
        create2DLineage(hmmCellDF,
                        attr='ATP_Class',
                        ylim=genMax,
                        attrMax=2,
                        savePath=saveDir_2dClass,
                        cmap='bwr')
    elif mode['Analysis']['hmmPrep']['class']['3d']:        
        saveDir_3dClass = os.path.join(saveDir,'Class_3dLin/')
        if hmmCellDF == None:
            hmmCellDF = hmm_prep(cellDFWP,lname=1,hname=3)
        hmmCellDF = lineage_editor(None,None,None,DF=hmmCellDF,mode=1)
        create3DLineage(hmmCellDF,
                        attr='ATP_Class',
                        attrMax=2,
                        attrMin=1,
                        savePath=saveDir_3dClass,
                        cmap='bwr')

        
        
        
    #save CellDF    
    if mode['cellDf']['save']:
        saveDir_CellDF = os.path.join(saveDir,'CellDf/CellDf.csv')
        cellDFWP.to_csv(saveDir_CellDF)
    #Prep oscillation
    if mode['Analysis']['oscillation']['prep']:
        saveDir_ATPIndi = os.path.join(saveDir, 'ATP_IndiCell/')
        write_ATPChange(cellDFWP,saveDir_ATPIndi)
    elif mode['Analysis']['oscillation']['fft']:
        csvPath = os.path.join(saveDir,"gprRes.csv")
        plot_IndiLine(csvPath,saveDir=saveDir,xlim=genMax)
    #Age   
    if mode['Analysis']['cellAge']:
        savePath = os.path.join(saveDir),'CellDf/CellDf_wAge.csv'
        if not os.path.isfile(savePath):
            cellDFWP = cellular_ageTracking(cellDFWP)
            cellDFWP.to_csv(savePath)
        else:
            cellDFWP = pd.read_csv(savePath)
        drawAgeFig(cellDFWP,saveDir=saveDir,atpMax=atpMax)
        


# ## Default Params

samplePath = {
    'poor':{
        'sample1':'/Users/nakatani/LAB/2019_M1/results/TmLps/samples/glc_poor/sample_1_1009_E1/Pos0',
        'sample2':'/Users/nakatani/LAB/2019_M1/results/TmLps/samples/glc_poor/sample_2_1223_E3/Pos0',
        'sample3':'/Users/nakatani/LAB/2019_M1/results/TmLps/samples/glc_poor/sample_3_1230_E6/Pos0'
         },
    'rich':{
        'sample1':'/Users/nakatani/LAB/2019_M1/results/TmLps/samples/glc_rich/sample_1_1016_2_E1/Pos0',
        'sample2':'/Users/nakatani/LAB/2019_M1/results/TmLps/samples/glc_rich/sample_2_1126_E4/Pos0',
        'sample3':'/Users/nakatani/LAB/2019_M1/results/TmLps/samples/glc_rich/sample_3_1203_E1/Pos0'
    }
}

'''
Paths for samples
poor_sample_1='/Users/nakatani/LAB/2019_M1/results/TmLps/samples/glc_poor/sample_1_1009_E1/Pos0'
poor_sample_2='/Users/nakatani/LAB/2019_M1/results/TmLps/samples/glc_poor/sample_2_1223_E3/Pos0'
poor_sample_3='/Users/nakatani/LAB/2019_M1/results/TmLps/samples/glc_poor/sample_3_1230_E6/Pos0'
rich_sample_1='/Users/nakatani/LAB/2019_M1/results/TmLps/samples/glc_rich/sample_1_1016_2_E1/Pos0'
rich_sample_2='/Users/nakatani/LAB/2019_M1/results/TmLps/samples/glc_rich/sample_2_1126_E4/Pos0'
rich_sample_3='/Users/nakatani/LAB/2019_M1/results/TmLps/samples/glc_rich/sample_3_1203_E1/Pos0'
'''

sampleNum = ['sample1','sample2','sample3']



if __name__ == "__main__":
    windows = ModeScreens()
    windows.run()
    if debug:
        print windows.getMode()
        print windows.getSamples()
        sys.exit(0)
    conditions = windows.getConditions()
    samples = windows.getSamples()
    mode = windows.getMode()
    for cond in conditions:
        for num in sampleNum:
            if samples[cond][num]:
                print "Doing " + cond + " " + num +"\n\t Path:"+samplePath[cond][num]
                Analysis_all(samplePath[cond][num],cond,num,mode,atpMax=atpMax,genMax=genMax)
