import pandas as pd
import numpy as np
import math
import matplotlib.pyplot as plt
from scipy import stats
import os
from tqdm import tqdm
from pyLineage.lineageIO.create2DLineage import create2DLineage

unk_age = -1
nan_age = 10

def drawAgeFig(CellDF,saveDir=None,ageMax=8,atpMax=None,Z=None):
    plt.cla()
    plt.clf()
    Age = CellDF[CellDF != pd.isnull(CellDF)][CellDF['Age']!= -1]
    if Z != None:
        Age = Age[Age['Z']==Z]
    Age = Age.dropna()
    plt.scatter(Age['Age'],Age['ATP'])
    plt.xlabel('Age')
    plt.ylabel('ATP mM')
    r, p = stats.spearmanr(Age['Age'], Age['ATP'])
    print(('r : ', r))
    print(('p : ', p))
    plt.title("R = " + str(r))
    if ageMax is None:
       ageMax =  max(Age['Age']) + 1
    if atpMax is None:
        atpMax = max(Age['ATP']) + 1
    plt.xlim((0,ageMax))
    plt.ylim((0,atpMax))
    if saveDir != None:
        plt.savefig(os.path.join(saveDir,"Age.png"))
    else:
        plt.show()

def find_distancePair(gDaughters, CellDF, mode="closest", originID=None):
    coordinates = list()
    origin_Cellxy = list()
    for uID in gDaughters['uID']:
        if uID != unk_age:
            tmp_cell = find_cell(uID, CellDF)
            coordinates.append((tmp_cell['uID'].values[0], tmp_cell['cenX'].values[0], tmp_cell['cenY'].values[0]))
    least_distance = (-3, -3, float('inf'))
    greatest_distance = (-3, -3, -float('inf'))

    if originID is not None:
        origin_cell = find_cell(originID, CellDF)
        origin_Cellxy = (originID, origin_cell['cenX'].values[0], origin_cell['cenY'].values[0])
    for xy in coordinates:
        if originID is not None and xy[0] != origin_Cellxy[0]:
            distance = ((xy[1] - origin_Cellxy[1]) ** 2 + (xy[2] - origin_Cellxy[2]) ** 2) ** 0.5
            if least_distance[2] > distance:
                least_distance = (xy[0], origin_Cellxy[0], distance)
            if greatest_distance[2] < distance:
                greatest_distance = (xy[0], origin_Cellxy[0], distance)
        else:
            subcoordinates = coordinates[coordinates.index(xy)+1:]
            if len(subcoordinates) == 0:
                break
            for subxy in subcoordinates:
                distance = ((xy[1] - subxy[1]) ** 2 + (xy[2] - subxy[2]) ** 2) ** 0.5
                if mode == "closest" and least_distance[2] > distance:
                    least_distance = (xy[0], subxy[0], distance)
                if mode == "farthest" and greatest_distance[2] < distance:
                    greatest_distance = (xy[0], subxy[0], distance)
    if mode == "closest":
        cDaughters = pd.DataFrame(columns=CellDF.columns.values)
        cDaughters = cDaughters.append(find_cell(least_distance[0], CellDF))
        cDaughters = cDaughters.append(find_cell(least_distance[1], CellDF))
        return cDaughters

    if mode == "farthest":
        fDaughters = pd.DataFrame(columns=CellDF.columns.values)
        fDaughters = fDaughters.append(find_cell(greatest_distance[0], CellDF))
        fDaughters = fDaughters.append(find_cell(greatest_distance[1], CellDF))
        return fDaughters


def find_cell(uID, CellDF):
    return CellDF[CellDF['uID'] == uID]

def daughter_timeMatch(gDaughter,CellDF,t):
    if int(gDaughter['Z']) >= t:
        while int(gDaughter['Z']) >= t:
            if int(gDaughter['Z']) == t:
                return gDaughter
            tmp = find_cell(gDaughter['motherID'].values[0], CellDF)
            if tmp is not None and not tmp.empty:
                gDaughter = tmp
    elif int(gDaughter['Z']) < t:
        while int(gDaughter['Z']) < t and int(gDaughter['daughter2ID']) == -2:
            tmp = find_cell(gDaughter['daughter1ID'].values[0], CellDF)
            if tmp is not None and not tmp.empty:
                gDaughter = tmp
                if int(gDaughter['Z']) == t:
                    return gDaughter
    return None

def findDaughter(daughter_cell,CellDF):
    while int(daughter_cell['daughter2ID']) == -2:
        tmp = find_cell(daughter_cell['daughter1ID'].values[0], CellDF)
        if tmp is not None and not tmp.empty:
            daughter_cell = tmp
        else:
            return None
    return daughter_cell

def find_grandDaughters(cell_slice, CellDF, t=None, mode=None):
    gDaughter1 = None
    gDaughter2 = None
    gDaughter3 = None
    gDaughter4 = None
    gDaughters = pd.DataFrame(columns=CellDF.columns.values)
    daughters = pd.DataFrame(columns=CellDF.columns.values)
    daughter_cell = cell_slice
    daughter_cell = findDaughter(daughter_cell,CellDF)
    daughter_cell1 = find_cell(daughter_cell['daughter1ID'].values[0], CellDF)
    daughter_cell2 = find_cell(daughter_cell['daughter2ID'].values[0], CellDF)


    if daughter_cell1 is not None and not daughter_cell1.empty:
        daughters = daughters.append(daughter_timeMatch(daughter_cell1,CellDF,t))
        daughter_cell1 = findDaughter(daughter_cell1,CellDF)
        gDaughter1 = find_cell(daughter_cell1['daughter1ID'].values[0], CellDF)
        gDaughter2 = find_cell(daughter_cell1['daughter2ID'].values[0], CellDF)
    if daughter_cell2 is not None and not daughter_cell2.empty:
        daughters = daughters.append(daughter_timeMatch(daughter_cell2,CellDF,t))
        daughter_cell2 = findDaughter(daughter_cell2,CellDF)
        gDaughter3 = find_cell(daughter_cell2['daughter1ID'].values[0], CellDF)
        gDaughter4 = find_cell(daughter_cell2['daughter2ID'].values[0], CellDF)
    if mode == "daughter":
        return daughters

    if t is None:
        if gDaughter1 is not None and gDaughter2 is not None:
            if not gDaughter1.empty:
                gDaughters = gDaughters.append(gDaughter1)
            if not gDaughter2.empty:
                gDaughters = gDaughters.append(gDaughter2)
        if gDaughter3 is not None and gDaughter4 is not None:
            if not gDaughter3.empty:
                gDaughters = gDaughters.append(gDaughter3)
            if not gDaughter4.empty:
                gDaughters = gDaughters.append(gDaughter4)
    else:
        t = int(t)
        if gDaughter1 is not None and not gDaughter1.empty:
            gDaughters = gDaughters.append(daughter_timeMatch(gDaughter1,CellDF,t))

        if gDaughter2 is not None and not gDaughter2.empty:
            gDaughters = gDaughters.append(daughter_timeMatch(gDaughter2,CellDF,t))

        if gDaughter3 is not None and not gDaughter3.empty:
            gDaughters = gDaughters.append(daughter_timeMatch(gDaughter3,CellDF,t))
            
        if gDaughter4 is not None and not gDaughter4.empty:
            gDaughters = gDaughters.append(daughter_timeMatch(gDaughter4,CellDF,t))

    return gDaughters


def find_parent(cell_slice, CellDF):
    mother_cell = cell_slice
    tmp_cell = find_cell(int(mother_cell['motherID']), CellDF)
    while tmp_cell is not None and not tmp_cell.empty:
        #print("Looking now @" + str(tmp_cell['uID']))
        #print(tmp_cell)
        if not tmp_cell['daughter2ID'].values[0] == -2:
            break
        tmp_cell = find_cell(int(tmp_cell['motherID']), CellDF)
    return tmp_cell


def fill_newcell(CellDF,timeinLin):
    tmpDF = CellDF[CellDF['Z'] == timeinLin]
    tmpDF = tmpDF[tmpDF['Age'].isnull()]    
    for uID in tmpDF['uID']:
        tmpCell = find_cell(uID, CellDF)
        if not tmpCell.empty and not math.isnan(tmpCell['Age'].values[0]):
            while tmpCell['daughter2ID'].values[0] == -2:
                duID = tmpCell['daughter1ID'].values[0]
                CellDF.loc[duID, 'Age'] = tmpCell['Age'].values[0]
                tmpCell = find_cell(duID, CellDF)
                if tmpCell.empty:
                    break
    return CellDF

def fill_pastcell(CellDF,timeinLin):
    tmpDF = CellDF[CellDF['Z']<=timeinLin]
    tmpDF = tmpDF[tmpDF['Age'].isnull()]
    for uID in tmpDF['uID']:
        tmpCell = find_cell(uID, CellDF)
        if not tmpCell.empty:
            mCell = find_cell(int(tmpCell['motherID']),CellDF)
            if int(mCell['Age']) >= 0:
                CellDF.loc[uID, 'Age'] = int(mCell['Age'])
            else:
                CellDF.loc[uID, 'Age'] = unk_age
    return CellDF


def check_overlap(closest_pair, farthest_pair):
    for cuID in closest_pair['uID']:
        for fuID in farthest_pair['uID']:
            if cuID == fuID:
                return False
    else:
        return True


def fill_nan_cells(CellDF,fill=True):
    if fill:
        tmpDF = CellDF[CellDF['Age'].isnull()]
        for uID in tmpDF['uID']:
            CellDF.loc[uID, 'Age'] = nan_age
    else:
        tmpDF = CellDF[CellDF['Age'].isnull()]
        for uID in tmpDF['uID']:
            CellDF.at[(CellDF['Age'] == nan_age),'Age'] = pd.np.nan
            
    return CellDF


def highlight_cell(uID, CellDF, attr):
    CellDF.loc[uID, attr] = 20
    return CellDF


def all_mothers(DF,CellDF):
    all_mothers = pd.DataFrame(columns=DF.columns.values)
    for uID in DF['uID']:
        tmp = find_cell(uID, CellDF)
        all_mothers = all_mothers.append(find_cell(tmp['motherID'], CellDF))
    return all_mothers


def cellular_ageTracking(CellDF, origin_frame=0, mode=None):
    CellDF['Age'] = np.nan
    for timeinLin in tqdm(list(range(origin_frame, max(CellDF['Z'])+1))):
        # print "Time:" + str(timeinLin)
        tmpDF = CellDF[CellDF['Z'] == timeinLin]
        tmpDF = tmpDF[tmpDF['Age'].isnull()]
        if not len(tmpDF) == 0:
            for uID in tmpDF['uID']:
                grand_daughters = pd.DataFrame(columns=CellDF.columns.values)
                if timeinLin == 0:
                    CellDF.loc[uID, 'Age'] = unk_age
                    #grand_daughters = find_grandDaughters(find_cell(uID, CellDF), CellDF, mode="daughter")
                else:
                    tmpcell = find_cell(uID, CellDF)
                    if not tmpcell.empty:
                        parent_cell = find_parent(tmpcell, CellDF)
                        if parent_cell is not None and not parent_cell.empty:
                            gParent_cell = find_parent(parent_cell, CellDF)
                            if gParent_cell is not None and not gParent_cell.empty:
                                grand_daughters = find_grandDaughters(gParent_cell, CellDF, t=timeinLin)
                if grand_daughters.shape[0] == 4:
                    closest_pair = find_distancePair(grand_daughters, CellDF)
                    farthest_pair = find_distancePair(grand_daughters, CellDF, mode="farthest")
                    if check_overlap(closest_pair, farthest_pair):
                        for cuID in closest_pair['uID']:
                            CellDF.loc[cuID, 'Age'] = 1
                        for fuID in farthest_pair['uID']:
                            this_cell = CellDF[CellDF['uID'] == fuID]
                            parent = find_parent(this_cell, CellDF)
                            parent_age = parent['Age'].values[0]
                            if not math.isnan(parent_age) and parent_age >= 0:
                                CellDF.loc[fuID, 'Age'] = parent_age + 1 #add age
                            else:
                                CellDF.loc[fuID, 'Age'] = unk_age #if no parent age is not known

                elif grand_daughters.shape[0] == 3:
                    main_cell = pd.DataFrame(columns=CellDF.columns.values)
                    for guID in grand_daughters['motherID']:
                        if grand_daughters['motherID'].value_counts()[guID] == 1:
                            main_cell = grand_daughters[grand_daughters['motherID'] == guID]
                            break
                    closest_pair = find_distancePair(grand_daughters, CellDF, originID=main_cell['uID'].values[0])
                    for guID in grand_daughters['uID']:
                        if guID in closest_pair['uID'].values:
                            if main_cell['uID'].values[0] != guID:
                                CellDF.loc[guID, 'Age'] = 1
                        elif guID != main_cell['uID'].values[0]:
                            parent = find_parent(find_cell(guID, CellDF), CellDF)
                            parent_age = parent['Age'].values[0]
                            if not parent.empty and parent_age != unk_age:
                                CellDF.loc[guID, 'Age'] = parent_age + 1 #add age
                            else:
                                #print guID
                                CellDF.loc[guID, 'Age'] = unk_age #if no parent, age is not known

        if mode == "debug":
            tmpDF = CellDF.copy()
            create2DLineage(fill_nan_cells(tmpDF),attr='Age')
        CellDF = fill_newcell(CellDF,timeinLin)
        CellDF = fill_pastcell(CellDF,timeinLin)
    return CellDF


if __name__ == "__main__":
    from annotateLineageIdx import annotateLineageIdx
    matFilePath = ('/Users/itabashi/Research/Analysis/Schnitzcells/'
                   '9999-99-99/488/data/488_lin.mat')
    segImgsPath = ('/Users/itabashi/Research/Analysis/Schnitzcells/'
                   '9999-99-99/488/segmentation/')
    rawImgsPath = ('/Users/itabashi/Research/Experiment/microscope/'
                   '2018/08/28/ECTC_8/Pos0/forAnalysis/488FS/')
    cellDfWPL = annotateLineageIdx(matFilePath, segImgsPath, rawImgsPath)
    cellDfWPL = cellular_ageTracking(cellDfWPL)
