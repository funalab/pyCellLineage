#!/usr/bin/env python
# coding: utf-8
# In[1]:
from pyCellLineage.lineageIO.measurePhenotypes import measurePhenotypes
from pyCellLineage.lineageIO.create3DLineage import create3DLineage
from pyCellLineage.lineageIO.create2DLineage import create2DLineage
from pyCellLineage.LIAnalysis.stochastic_hmm import hmm_prep
from pyCellLineage.lineageIO.getIndependentLineage import getIndependentLineage
from pyCellLineage.LIAnalysis.fftAnalysis import write_ATPChange
from pyCellLineage.LIAnalysis.cellular_ageTracking import cellular_ageTracking
from pyCellLineage.lineageIO.createHist import createHistMovie
from pyCellLineage.lineageIO.createHist import createHist
from pyCellLineage.LIAnalysis.cellular_ageTracking import drawAgeFig
from pyCellLineage.LIAnalysis.fftAnalysis import plot_IndiLine
from pyCellLineage.lineageIO.lineage_editor import lineage_editor
from pyCellLineage.Analysis_Gui.Final_Analysis_GUI_Class import ModeScreens
from pyCellLineage.Analysis_Gui.modeIO import modeIO
from pyCellLineage.Analysis_Gui.path_prep import path_prep ## Works only for a specific directory structure(check examples)
from pyCellLineage.lineageIO.Total_ATP import Total_ATP
from pyCellLineage.PDAnalysis.nineFivePercentile import nineFivePercentile
from pyCellLineage.Analysis_Gui.pathParms import pathParms
from pyCellLineage.PDAnalysis.findBestBIC import findBestBIC

import numpy as np
import os
import pandas as pd
import sys

'''
Author: Ryo Nakatani
Runs Analysis based on GUI selected modes 
Can analyze based on cellular age, FFT(Uses R for GPR), Stochastic Analysis(Uses R for HMM), and Spacial Correlation(Uses Matlab).
'''


# Magic Numbers
atpMax = 10
genMax = 35
debug = False


def Analysis_all(path,instMode,thr=None,atpMax=None,genMax=None):
    hmmCellDF = None
    paths = path_prep(path)
    cellDFWP = measurePhenotypes(paths['matFilePath'], paths['segImgsPath'], paths['rawImgsPath'])        
    #parent of path
    mode = dict(instMode.getMode())
    
    saveDir = str('/'.join(os.path.abspath(path).split('/')[0:-1-0]))

    #Make Hist    
    if mode['hist']['normal']:
        saveDir_hist = os.path.join(saveDir,'Hist/')
        createHistMovie(cellDFWP,atpMax=atpMax,saveDir=saveDir_hist)
    elif mode['hist']['totalATP']:
        totalDF = Total_ATP(instMode=instMode)
        saveDir_hist = os.path.join(saveDir,'totalATP_Hist/')
        createHist(totalDF,atpMax=atpMax,saveDir=saveDir_hist)
        sys.exit(0)
    elif mode['hist']['totalRich']:
        totalDF = Total_ATP(instMode=instMode,glcPoor=False,num=100)
        saveDir_hist = os.path.join(saveDir,'totalRichATP_Hist/')
        createHist(totalDF,atpMax=atpMax,saveDir=saveDir_hist)
        sys.exit(0)
    elif mode['hist']['totalPoor']:
        totalDF = Total_ATP(instMode=instMode,glcRich=False,num=100)
        saveDir_hist = os.path.join(saveDir,'totalPoorATP_Hist/')
        createHist(totalDF,atpMax=atpMax,saveDir=saveDir_hist)
        sys.exit(0)
        
    #make lineage
    if mode['lineage']['save']:
        savePathLin = os.path.join(saveDir,"lineage.pdf")
        create2DLineage(cellDFWP,attr='intensity',attrMax=atpMax, ylim=genMax,savePath=savePathLin)
    elif mode['lineage']['show']:
        create2DLineage(cellDFWP,attr='intensity',attrMax=atpMax, ylim=genMax)
    elif mode['lineage']['3d']:
        saveDir_3d = os.path.join(saveDir,'3dLin')
        create3DLineage(lineage_editor(None,None,None,DF=cellDFWP,mode=1),
                        attr='intensity',
                        attrMax=atpMax,
                        savePath=saveDir_3d)
    else:
        create2DLineage(cellDFWP,attr='intensity',attrMax=atpMax, ylim=genMax,show=False)
    #prepHmm
    if mode['hmmPrep']['normal']['mean']:
        saveDir_Indi = os.path.join(saveDir, 'IndiCell/')
        cellDFWP = hmm_prep(cellDFWP,save_dir=saveDir_Indi,lname="low",hname="high")
        hmmCellDF = cellDFWP
    elif mode['hmmPrep']['normal']['median']:
        saveDir_Indi = os.path.join(saveDir, 'IndiCellMedian/')
        thr = 'Median'
        cellDFWP = hmm_prep(cellDFWP,thr=thr,save_dir=saveDir_Indi,lname="low",hname="high")
        hmmCellDF = cellDFWP
    elif mode['hmmPrep']['totalATP']['mean']:
        if thr == None:
            totalDF = Total_ATP(instMode=instMode)
            thr = sum(totalDF['intensity'])/len(totalDF['intensity'])
        saveDir_Indi = os.path.join(saveDir, 'IndiCellTotal/')            
        cellDFWP = hmm_prep(cellDFWP,save_dir=saveDir_Indi,thr=thr,lname="low",hname="high")
        hmmCellDF = cellDFWP
    elif mode['hmmPrep']['totalATP']['median']:
        saveDir_Indi = os.path.join(saveDir, 'IndiCellTotal/')
        if thr == None:
            totalDF = Total_ATP(instMode=instMode)
            thr = totalDF['intensity'].median()
        cellDFWP = hmm_prep(cellDFWP,save_dir=saveDir_Indi,thr=thr,lname="low",hname="high")
        hmmCellDF = cellDFWP
    elif mode['hmmPrep']['totalATP']['gmmPoor']:
        if thr == None:
            totalDF = Total_ATP(samples={},glcRich=False)
            thr = findBestBIC(totalDF['intensity'])
        saveDir_Indi = os.path.join(saveDir, 'IndiCellGMM/')            
        cellDFWP = hmm_prep(cellDFWP,save_dir=saveDir_Indi,thr=thr,lname="low",hname="high")
        hmmCellDF = cellDFWP
    elif mode['hmmPrep']['95ATP']['both']:
        if thr == None:
            totalDF = Total_ATP(instMode=instMode)
            thr = nineFivePercentile(totalDF,attr='intensity')
        saveDir_Indi = os.path.join(saveDir, 'IndiCellPercentile/')        
        cellDFWP = hmm_prep(cellDFWP,save_dir=saveDir_Indi,thr=thr,lname="low",hname="high")        
        hmmCellDF = cellDFWP
    elif mode['hmmPrep']['95ATP']['control']:
        if thr == None:
            totalDF = Total_ATP(instMode=instMode,glcPoor=False)
            thr = nineFivePercentile(totalDF)
        saveDir_Indi = os.path.join(saveDir, 'IndiCellPercentile/')        
        cellDFWP = hmm_prep(cellDFWP,save_dir=saveDir_Indi,thr=thr,lname="low",hname="high")        
        hmmCellDF = cellDFWP
        
    if mode['hmmPrep']['class']['2d']:
        saveDir_2dClass = os.path.join(saveDir,'Class_2dLin.pdf')
        hmmCellDF = hmm_prep(cellDFWP,thr=thr,lname="low",hname="high")
        create2DLineage(hmmCellDF,
                        attr='ATP_Class',
                        ylim=genMax,
                        savePath=saveDir_2dClass)
    elif mode['hmmPrep']['class']['3d']:        
        saveDir_3dClass = os.path.join(saveDir,'Class_3dLin/')
        hmmCellDF = hmm_prep(cellDFWP,thr=thr,lname="low",hname="high")
        hmmCellDF = lineage_editor(None,None,None,DF=hmmCellDF,mode=1)
        create3DLineage(hmmCellDF,
                        attr='ATP_Class',
                        savePath=saveDir_3dClass,
                        degree=180)
        
        
        
    #save CellDF    
    if mode['cellDf']['save']:
        saveDir_CellDF = os.path.join(saveDir,'CellDf.csv')
        cellDFWP.to_csv(saveDir_CellDF)
    #Prep oscillation
    if mode['oscillation']['prep']:
        saveDir_ATPIndi = os.path.join(saveDir, 'ATP_IndiCell/')
        write_ATPChange(cellDFWP,saveDir_ATPIndi,changedCSVpath=paths['changeCSV'])
    elif mode['oscillation']['fft']:
        csvPath = os.path.join(saveDir,"gprRes.csv")
        plot_IndiLine(csvPath,saveDir=saveDir,xlim=genMax)
    #Age
    if mode['cellAge']['save']:
        savePath = os.path.join(saveDir,'CellDf_wAge.csv')
        if not os.path.isfile(savePath):
            print ("Couldn't find csv("+savePath+")\n Creating a New One\n\t This may take a while...\n")
            cellDFWP = cellular_ageTracking(cellDFWP)
            cellDFWP.to_csv(savePath)
        else:
            cellDFWP = pd.read_csv(savePath)
        drawAgeFig(cellDFWP,saveDir=saveDir,atpMax=atpMax)

def run():
    sampleNum = ['sample1','sample2','sample3']
    samplePath = pathParms().getSamplePath()
    
    windows = ModeScreens()
    windows.run()
    if debug:
        print(windows.getMode())
        print(windows.getSamples())
        sys.exit(0)
    conditions = windows.getConditions()
    samples = dict(windows.getSamples())
    mode = dict(windows.getMode())
    thr = None
    if mode['hmmPrep']['totalATP']['mean']:
        totalDF = Total_ATP(instMode=windows)
        thr = sum(totalDF['intensity'])/len(totalDF['intensity'])
    elif mode['hmmPrep']['95ATP']['both'] or mode['hmmPrep']['95ATP']['control']:
        totalDF = Total_ATP(instMode=windows)
        thr = nineFivePercentile(totalDF)
    elif mode['hmmPrep']['totalATP']['gmmPoor']:
        totalDF = Total_ATP(glcRich=False)
        thr = findBestBIC(totalDF['intensity'])
        print ("Found GMM thr to be " + str(thr) + "\n")

    for cond in conditions:
        for num in sampleNum:
            if samples[cond][num]:
                print ("Doing " + cond + " " + num +"\n\t Path:"+samplePath[cond][num])
                Analysis_all(samplePath[cond][num],windows,thr=thr,atpMax=atpMax,genMax=genMax)
    

if __name__ == "__main__":
    run()
