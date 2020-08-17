import pandas as pd
import numpy as np
import math
import matplotlib.pyplot as plt
from scipy import stats
import os

unk_age = -1
nan_age = 10

def drawAgeFig(CellDF,saveDir=None,ageMax=None,atpMax=None):
    plt.cla()
    plt.clf()
    Age = CellDF[CellDF != pd.isnull(CellDF)][CellDF['Age']!= -1]
    Age = Age[Age['Z']==max(Age['Z'])]
    Age = Age.dropna()
    plt.scatter(Age['Age'],Age['ATP'])
    plt.xlabel('Age')
    plt.ylabel('ATP mM')
    r, p = stats.spearmanr(Age['Age'], Age['ATP'])
    print('r : ', r)
    print('p : ', p)
    plt.title("R = " + str(r))
    if ageMax is None:
       ageMax =  max(Age['Age']) + 1
    if atpMax is None:
        atpMax = max(Age['ATP']) + 1
    plt.xlim(0,ageMax)
    plt.ylim(0,atpMax)
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


def find_grandDaughters(cell_slice, CellDF, t=None, mode=None):
    gDaughter1 = None
    gDaughter2 = None
    gDaughter3 = None
    gDaughter4 = None
    gDaughters = pd.DataFrame(columns=CellDF.columns.values)
    daughters = pd.DataFrame(columns=CellDF.columns.values)
    daughter_cell = cell_slice
    while daughter_cell['daughter2ID'].values[0] == -2:
        daughter_cell = find_cell(daughter_cell['daughter1ID'].values[0], CellDF)
    daughter_cell1 = find_cell(daughter_cell['daughter1ID'].values[0], CellDF)
    daughter_cell2 = find_cell(daughter_cell['daughter2ID'].values[0], CellDF)
    if not daughter_cell1.empty:
        if mode == "daughter":
            if t is not None and daughter_cell1['Z'].values[0] <= t:
                while daughter_cell1['Z'].values[0] != t:
                    daughter_cell1 = fing_cell(daughter_cell1['daughter1ID'].values[0], CellDF)
            daughters = daughters.append(daughter_cell1)
        while True:
            tmp = find_cell(daughter_cell1['daughter1ID'].values[0], CellDF)
            if tmp is not None and not tmp.empty:
                daughter_cell1 = tmp
            else:
                break
            if int(daughter_cell1['daughter2ID']) != -2:
                break
        gDaughter1 = find_cell(daughter_cell1['daughter1ID'].values[0], CellDF)
        gDaughter2 = find_cell(daughter_cell1['daughter2ID'].values[0], CellDF)
    if not daughter_cell2.empty:
        if mode == "daughter":
            if t is not None and daughter_cell2['Z'].values[0] <= t:
                while daughter_cell2['Z'].values[0] != t:
                    daughter_cell2 = fing_cell(daughter_cell2['daughter1ID'].values[0], CellDF)
            daughters = daughters.append(daughter_cell2)
        while True:
            tmp = find_cell(daughter_cell2['daughter1ID'].values[0], CellDF)
            if tmp is not None and not tmp.empty:
                daughter_cell2 = tmp
            else:
                break
            if int(daughter_cell2['daughter2ID']) != -2:
                break
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
            if int(gDaughter1['Z']) > t:
                gDaughter1 = daughter_cell1
                while int(gDaughter1['Z']) > t:
                    tmp = find_cell(gDaughter1['motherID'].values[0], CellDF)
                    if tmp is not None and not tmp.empty:
                        gDaughter1 = tmp
                    else:
                        break
            while int(gDaughter1['Z']) <= t:
                tmp = find_cell(gDaughter1['daughter1ID'].values[0], CellDF)
                if tmp is not None and not tmp.empty:
                    gDaughter1 = tmp
                else:
                    break
            gDaughters = gDaughters.append(gDaughter1)

        if gDaughter2 is not None and not gDaughter2.empty:
            if gDaughter2['Z'].values[0] <= t:
                while int(gDaughter2['Z']) < t:
                    tmp = find_cell(gDaughter2['daughter1ID'].values[0], CellDF)
                    if tmp is not None and not tmp.empty:
                        gDaughter2 = tmp
                    else:
                        break
                gDaughters = gDaughters.append(gDaughter2)

        if gDaughter3 is not None and not gDaughter3.empty:
            if gDaughter3['Z'].values[0] > t:
                gDaughter3 = daughter_cell2
                while int(gDaughter3['Z']) > t:
                    tmp = find_cell(gDaughter3['motherID'].values[0], CellDF)
                    if tmp is not None and not tmp.empty:
                        gDaughter3 = tmp
                    else:
                        break

            while int(gDaughter3['Z']) <= t:
                tmp = find_cell(gDaughter3['daughter1ID'].values[0], CellDF)
                if tmp is not None and not tmp.empty:
                    gDaughter3 = tmp
                else:
                    break
            gDaughters = gDaughters.append(gDaughter3)

        if gDaughter4 is not None and not gDaughter4.empty:
            if gDaughter4['Z'].values[0] <= t:
                while int(gDaughter4['Z']) < t:
                    tmp = find_cell(gDaughter4['daughter1ID'].values[0], CellDF)
                    if tmp is not None and not tmp.empty:
                        gDaughter4 = tmp
                    else:
                        break
                gDaughters = gDaughters.append(gDaughter4)

    return gDaughters


def find_parent(cell_slice, CellDF):
    mother_cell = cell_slice
    while True:
        tmp_cell = find_cell(mother_cell['motherID'].values[0], CellDF)
        if not tmp_cell.empty:
            mother_cell = tmp_cell
        else:
            break
        if mother_cell['daughter2ID'].values[0] != -2:
            break
    return mother_cell


def fill_newcell(CellDF):
    for uID in CellDF['uID']:
        tmpCell = find_cell(uID, CellDF)
        if not tmpCell.empty and not math.isnan(tmpCell['Age'].values[0]):
            while tmpCell['daughter2ID'].values[0] == -2:
                duID = tmpCell['daughter1ID'].values[0]
                if duID != unk_age:
                    CellDF.loc[duID, 'Age'] = tmpCell['Age'].values[0]
                tmpCell = find_cell(duID, CellDF)
                if tmpCell.empty:
                    break
    return CellDF


def check_overlap(closest_pair, farthest_pair):
    for cuID in closest_pair['uID']:
        for fuID in farthest_pair['uID']:
            if cuID == fuID:
                return False
    else:
        return True


def fill_nan_cells(CellDF):
    tmpDF = CellDF[CellDF['Age'].isnull()]
    for uID in tmpDF['uID']:
        CellDF.loc[uID, 'Age'] = nan_age
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
    CellDF['Age'] = pd.np.nan
    for timeinLin in range(origin_frame, max(CellDF['Z'])):
        tmpDF = CellDF[CellDF['Z'] == timeinLin]
        tmpDF = tmpDF[tmpDF['Age'].isnull()]
        for uID in tmpDF['uID']:
            grand_daughters = pd.DataFrame(columns=CellDF.columns.values)
            if timeinLin == 0:
                if uID != unk_age:
                    #print uID
                    CellDF.loc[uID, 'Age'] = unk_age
                grand_daughters = find_grandDaughters(find_cell(uID, CellDF), CellDF, mode="daughter")
            else:
                tmpcell = find_cell(uID, CellDF)
                if not tmpcell.empty:
                    parent_cell = find_parent(tmpcell, CellDF)
                    if not parent_cell.empty:
                        gParent_cell = find_parent(parent_cell, CellDF)
                        if not gParent_cell.empty:
                            grand_daughters = find_grandDaughters(gParent_cell, CellDF, t=timeinLin)
                        else:
                            grand_daughters = find_grandDaughters(parent_cell, CellDF, t=timeinLin, mode="daughter")
                    else:
                        grand_daughters = find_grandDaughters(parent_cell, CellDF, t=timeinLin, mode="daughter")
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
                        if not math.isnan(parent_age) and parent_age != unk_age:
                            CellDF.loc[fuID, 'Age'] = parent_age + 1
                        elif fuID != unk_age:
                            #print fuID
                            CellDF.loc[fuID, 'Age'] = unk_age

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
                            CellDF.loc[guID, 'Age'] = parent_age + 1
                        elif guID != unk_age:
                            #print guID
                            CellDF.loc[guID, 'Age'] = unk_age

            elif grand_daughters.shape[0] == 2 and uID != unk_age:
                CellDF.loc[uID, 'Age'] = unk_age
            CellDF = fill_newcell(CellDF)
    if mode == "debug":
        CellDF = fill_nan_cells(CellDF)
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
