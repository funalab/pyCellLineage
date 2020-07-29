"""
Author: Joel Nakatani
Overview:

Parameters:
"""


class modeIO():
    Names = list()
    mode = dict()
    output = False
    dictList = dict()


    def __init__(self,mode):
        self.mode = mode
        if self.output:
            self.modeOutput(self.mode,0)
        self.modeSave(self.mode,0,list())

    def setOutputBool(self,Bool):
        self.output = Bool
        return

    def getModeNames(self):
        return self.Names

    def modeOutput(self,mode,depth):
        for modeName in mode.keys():
            space = "\t" * depth
            print space + modeName
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
            for modeName in mode.keys():
                name.append(modeName)
                self.modeSave(mode[modeName],depth + 1,name)
                name = name[:depth]
        return
