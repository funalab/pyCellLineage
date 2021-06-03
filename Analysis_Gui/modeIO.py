"""
Author: Joel Nakatani
Overview:
Class for Mode Input and Output
Reads from files, and saves Mode settings for Analysis

Parameters:
"""
import json
import os
import pyLineage.Analysis_Gui as myPackage

class modeIO():
    Names = list()
    mode = {
        'lineage':{
            '3d':False,
            'save':False,
            'show':False,
        },
        'cellDf':{
            'save':False
        },
        'cellAge':{
            'save':False
        },
        'oscillation':{
            'prep':False,
            'fft':False
        },
        'hist':{
            'totalATP':False,
            'totalRich':False,
            'totalPoor':False,
            'normal':False
        },
        'hmmPrep':{
            'normal':{
                'mean':False,
                'median':False
            },
            'totalATP':{
                'mean':False,
                'gmmPoor':False
            },
            '95ATP':{
                'both':False,
                'control':False
            },
            'class':{
                '2d':False,
                '3d':False
            }
        }
    }
    output = False
    dictList = dict()
    defaultPath = str()
    samples = {
        'poor':{
            'sample1':True,
            'sample2':True,
            'sample3':True
        },
        'rich':{
            'sample1':True,
            'sample2':True,
            'sample3':True
        }
    }
    conditions = ['poor','rich']



    def __init__(self):
        if self.output:
            self.modeOutput(self.mode,0)
        self.modeSave(self.mode,0,list())
        self.defaultPath = os.path.join(os.path.dirname(myPackage.__file__),".modeconfig")

    def setOutputBool(self,Bool):
        self.output = Bool
        return

    def getModeNames(self):
        return self.Names

    def getMode(self):
        return self.mode

    def setMode(self,mode):
        self.mode = mode

    def getSamples(self):
        return self.samples

    def getConditions(self):
        return self.conditions
    
    def modeOutput(self,mode,depth):
        for modeName in list(mode.keys()):
            space = "\t" * depth
            print((space + modeName))
            if type(mode[modeName]) is not type(True):
                self.modeOutput(mode[modeName],depth + 1)
        return
    
    def splitModeNames(self):
        currMode = None
        modeLists = list()
        dictL = dict()
        for spmodeName in self.Names:
            if currMode == None:
                currMode = spmodeName[:-1]
            elif spmodeName[:-1] != currMode:
                dictL[" ".join(currMode)] = modeLists
                #reset everything
                currMode = spmodeName[:-1]
                modeLists = list()
            modeLists.append(spmodeName[-1])
        self.dictList = dictL
        return self.dictList
    
    def modeSave(self,mode,depth,name):
        if type(mode) == type(True):
            self.Names.append(name)
        else:
            for modeName in list(mode.keys()):
                name.append(modeName)
                self.modeSave(mode[modeName],depth + 1,name)
                name = name[:depth]
        return

    def modeRead(self,FileName=None):
        if FileName == None:
            FileName = self.DefaultPath
        if os.path.isfile(FileName):
            with open(FileName) as f:
                df = json.load(f)
        else:
            print("Can't find File")
            df = None
        return df

    def modeWrite(self,df,FileName=None):
        if FileName == None:
            FileName = self.DefaultPath
        with open(FileName,'w') as f:
            json.dump(df,f)
        
