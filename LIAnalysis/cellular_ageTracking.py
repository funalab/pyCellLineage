import pandas as pd
import numpy as np


def find_distancePair(gDaughters, CellDF, mode="closest", originID=None):
    coordinates = list()
    origin_Cellxy = None
    for uID in gDaughters['uID']:
        tmp_cell = find_cell(uID, CellDF)
        coordinates.append((tmp_cell['uID'].values[0], tmp_cell['cenX'].values[0], tmp_cell['cenY'].values[0]))
    least_distance = (-3, -3, float('inf'))
    greatest_distance = (-3, -3, 0)

    if originID is not None:
        origin_cell = find_cell(originID, CellDF)
        origin_Cellxy = (originID, origin_cell['cenX'].values[0], origin_cell['cenY'].values[0])
    for xy in coordinates:
        if originID is not None:
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
        fDaughters = fDaughters.apend(find_cell(greatest_distance[1], CellDF))
        return fDaughters


def find_cell(uID, CellDF):
    return CellDF[CellDF['uID'] == uID]


def find_grandDaughters(cell_slice, CellDF, t=None):
    gDaughter1 = None
    gDaughter2 = None
    gDaughter3 = None
    gDaughter4 = None
    gDaughters = pd.DataFrame(columns=CellDF.columns.values)
    daughter_cell = cell_slice
    while daughter_cell['daughter1ID'].values[0] == -2 or daughter_cell['daughter2ID'].values[0] == -2:
        daughter_cell = find_cell(daughter_cell['daughter1ID'].values[0], CellDF)

    daughter_cell1 = find_cell(daughter_cell['daughter1ID'].values[0], CellDF)
    daughter_cell2 = find_cell(daughter_cell['daughter2ID'].values[0], CellDF)
    if not daughter_cell1.empty:
        gDaughter1 = find_cell(daughter_cell1['daughter1ID'].values[0], CellDF)
        gDaughter2 = find_cell(daughter_cell1['daughter2ID'].values[0], CellDF)
    if not daughter_cell2.empty:
        gDaughter3 = find_cell(daughter_cell2['daughter1ID'].values[0], CellDF)
        gDaughter4 = find_cell(daughter_cell2['daughter2ID'].values[0], CellDF)

    if t is None:
        if gDaughter1 is not None and gDaughter2 is not None:
            if not gDaughter1.empty:
                gDaughters = gDaughters.append(gDaughter1)
            if not gDaughter2.empty:
                gDaughters = gDaughters.append(gDaughter2)
        if gDaughter3 is not None and gDaughter4 is not None:
            if not gDaughter3.empty:
                gDaughters = gDaughters.append(gDaughter3)
            if not not gDaughter4.empty:
                gDaughters = gDaughters.append(gDaughter4)
    else:
        if gDaughter1['Z'] == t:
            gDaughters = gDaughters.append(gDaughter1)
        if gDaughter2['Z'] == t:
            gDaughters = gDaughters.append(gDaughter2)
        if gDaughter3['Z'] == t:
            gDaughters = gDaughters.append(gDaughter3)
        if gDaughter4['Z'] == t:
            gDaughters = gDaughters.append(gDaughter4)
    return gDaughters


def find_parent(cell_slice, CellDF):
    uID = cell_slice['motherID'].values[0]
    parent = CellDF[CellDF['uID'] == uID]
    return parent


def cellular_ageTracking(CellDF):
    CellDF['Age'] = pd.np.nan
    for timeinLin in range(max(CellDF['Z'])):
        tmpDF = CellDF[CellDF['Z'] == timeinLin]
        if timeinLin == 0:
            for uID in tmpDF['uID']:
                tmpCell = find_cell(uID, CellDF)
                CellDF.loc[uID, 'Age'] = pd.np.nan
                gDaughters = find_grandDaughters(tmpCell, CellDF)
                print gDaughters
                cDaughters = find_distancePair(gDaughters, CellDF)
                for cuID in cDaughters['uID']:
                    CellDF.loc[cuID, 'Age'] = 1
        else:
            undecided_cells = tmpDF[tmpDF['Age'] == pd.np.nan]
            if len(undecided_cells) != 0:
                for uID in undecided_cells['uID']:
                    tmpcell = find_cell(uID, CellDF)
                    parent_cell = find_parent(tmpcell, CellDF)
                    gParent_cell = find_parent(parent_cell, CellDF)
                    grand_daughters = find_grandDaughters(gParent_cell, CellDF, t=timeinLin)
                    if len(grand_daughters) == 4:
                        closest_pair = find_distancePair(grand_daughters, CellDF)
                        farthest_pair = find_distancePair(grand_daughters, CellDF, mode="farthest")
                        # add check if no overlaps later
                        for cuID in closest_pair['uID']:
                            CellDF.loc[cuID, 'Age'] = 1
                        for fuID in farthest_pair['uID']:
                            cell = CellDF[CellDF['uID'] == fuID]
                            parent = find_parent(cell)
                            parent_age = parent['Age'].values[0]
                            if parent_age != pd.np.nan:
                                CellDF.loc[fuID, 'Age'] = parent_age + 1
                            else:
                                CellDF.loc[fuID, 'Age'] = pd.np.nan
                    else:
                        mother = None
                        for uID in grand_daughters['uID']:
                            cell = find_cell(uID, CellDF)
                            if mother != cell['motherID'].values[0] and mother is not None:
                                mother = cell['motherID'].values[0]
                                main_cell = find_cell(mother, CellDF)
                                break
                            mother = cell['motherID'].vaues[0]
                        closest_pair = find_distancePair(grand_daughters, CellDF, originID=main_cell['uID'].values[0])
                        for cuID in closest_pair['uID']:
                            tmp_cell = find_cell(cuID, CellDF)
                            if tmp_cell['uID'].values[0] != main_cell['uID'].values[0]:
                                CellDF.loc[cuID, 'Age'] = 1

        undecided_cells = tmpDF[tmpDF['Age'] == pd.np.nan]  # fill ages for unchanging cells
        for uID in undecided_cells['uID']:
            tmp_cell = find_cell(uID, CellDF)
            while tmp_cell['daughter1ID'].values[0] == -2 or tmp_cell['daughter2ID'].values[0] == -2:
                tmp_cell = find_parent(tmp_cell, CellDF)
            CellDF.loc[uID, 'Age'] = tmp_cell['Age'].values[0]
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
    cellular_ageTracking(cellDfWPL)


