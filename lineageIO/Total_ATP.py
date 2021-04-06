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

# from pyLineage.Analysis_Gui.Final_Analysis_GUI_Class import ModeScreens
# from pyLineage.Analysis_Gui.modeIO import modeIO
# from pyLineage.Analysis_Gui.path_prep import path_prep ## Works only for a specific directory structure(check examples)
# from pyLineage.Analysis_Gui.pathParms import pathParms
# from pyLineage.Analysis_Gui.Final_Analysis_GUI_Class import *

import numpy as np
import os
import pandas as pd
import sys
import copy

def Total_ATP(instMode=None,samples=None,conditions=None,cellDFWP=None,glcRich=True,glcPoor=True):
    sampleNum = ['sample1','sample2','sample3']
    samplePath = dict(pathParms().getSamplePath())

    if cellDFWP != None:
        totalDF = pd.DataFrame(columns=cellDFWP.columns)
    else:
        totalDF = None
        
    # if instMode == None:
    #     default = ModeScreens()
    # else:
    default = instMode
        
    if samples == None:
        samples = dict(default.getSamples())

    tmp = copy.deepcopy(samples)
    if conditions == None:
        conditions = default.getConditions()
            
    if not glcRich:
        for key in sampleNum:
            tmp['rich'][key] = False
    if not glcPoor:
        for key in sampleNum:
            tmp['poor'][key] = False        

    for cond in conditions:
        for num in sampleNum:
            if tmp[cond][num]:
                paths = path_prep(samplePath[cond][num])
                CellDF = measurePhenotypes(paths['matFilePath'], paths['segImgsPath'], paths['rawImgsPath'])        
                totalDF = pd.concat([totalDF,CellDF])
    return totalDF
