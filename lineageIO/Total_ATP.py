# In[1]:
from .measurePhenotypes import measurePhenotypes
from .create3DLineage import create3DLineage
from .create2DLineage import create2DLineage
from ..LIAnalysis.stochastic_hmm import hmm_prep
from .getIndependentLineage import getIndependentLineage
from ..LIAnalysis.fftAnalysis import write_ATPChange
from ..LIAnalysis.cellular_ageTracking import cellular_ageTracking
from .createHist import createHistMovie
from .createHist import createHist
from ..LIAnalysis.cellular_ageTracking import drawAgeFig
from ..LIAnalysis.fftAnalysis import plot_IndiLine
from .lineage_editor import lineage_editor

from ..Analysis_Gui.Final_Analysis_GUI_Class import ModeScreens
from ..Analysis_Gui.modeIO import modeIO
from ..Analysis_Gui.path_prep import path_prep ## Works only for a specific directory structure(check examples)
from ..Analysis_Gui.pathParms import pathParms
from ..Analysis_Gui.Final_Analysis_GUI_Class import *

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
