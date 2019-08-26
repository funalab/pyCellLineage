import pandas as pd
import numpy as np


unk_age = -1


def find_distancePair(gDaughters, CellDF, mode="closest", originID=None):
    coordinates = list()
    origin_Cellxy = list()
    for uID in gDaughters['uID']:
        tmp_cell = find_cell(uID, CellDF)
        coordinates.append((tmp_cell['uID'].values[0], tmp_cell['cenX'].values[0], tmp_cell['cenY'].values[0]))
    least_distance = (-3, -3, float('inf'))
    greatest_distance = (-3, -3, -1)

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
        fDaughters = fDaughters.apend(find_cell(greatest_distance[1], CellDF))
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
    while True:
        daughter_cell = find_cell(daughter_cell['daughter1ID'].values[0], CellDF)
        if daughter_cell['daughter2ID'].values[0] != -2:
            break
    daughter_cell1 = find_cell(daughter_cell['daughter1ID'].values[0], CellDF)
    daughter_cell2 = find_cell(daughter_cell['daughter2ID'].values[0], CellDF)
    if not daughter_cell1.empty:
        if mode == "daughter":
            if t is not None and daughter_cell1['Z'].values[0] <= t:
                while daughter_cell1['Z'].values[0] != t:
                    daughter_cell1 = fing_cell(daughter_cell1['daughter1ID'].values[0], CellDF)
            daughters = daughters.append(daughter_cell1)
        while True:
            daughter_cell1 = find_cell(daughter_cell1['daughter1ID'].values[0], CellDF)
            if daughter_cell1['daughter2ID'].values[0] != -2:
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
            daughter_cell2 = find_cell(daughter_cell2['daughter1ID'].values[0], CellDF)
            if daughter_cell2['daughter2ID'].values[0] != -2:
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
            if not not gDaughter4.empty:
                gDaughters = gDaughters.append(gDaughter4)
    else:
        if gDaughter1 is not None and not gDaughter1.empty:
            if gDaughter1['Z'].values[0] <= t:
                while gDaughter1['Z'].values[0] != t:
                    gDaughter1 = find_cell(gDaughter1['daughter1ID'].values[0], CellDF)
                gDaughters = gDaughters.append(gDaughter1)
            else:
                for uID in daughters['uID']:
                    if uID != gDaughter1['motherID'].values[0] and uID not in gDaughters['uID'].values:
                        gDaughters = gDaughters.append(find_cell(uID, CellDF))
                        break
        if gDaughter2 is not None and not gDaughter2.empty:
            if gDaughter2['Z'].values[0] <= t:
                while gDaughter2['Z'].values[0] != t:
                    gDaughter2 = find_cell(gDaughter2['daughter1ID'].values[0], CellDF)
                gDaughters = gDaughters.append(gDaughter2)
            else:
                for uID in daughters['uID']:
                    if uID != gDaughter2['motherID'].values[0] and uID not in gDaughters['uID'].values:
                        gDaughters = gDaughters.append(find_Cell(uID, CellDF))
                        break
        if gDaughter3 is not None and not gDaughter3.empty:
            if gDaughter3['Z'].values[0] <= t:
                while gDaughter3['Z'].values[0] != t:
                    gDaughter3 = find_cell(gDaughter3['daughter1ID'].values[0], CellDF)
                gDaughters = gDaughters.append(gDaughter3)
            else:
                for uID in daughters['uID']:
                    if uID != gDaughters3['motherID'].values[0] and uID not in gDaughters['uID'].values:
                        gDaughters = gDaughters.append(find_Cell(uID, CellDF))
                        break
        if gDaughter4 is not None and not gDaughter4.empty:
            if gDaughter4['Z'].values[0] <= t:
                while gDaughter3['Z'].values[0] != t:
                    gDaughter4 = find_cell(gDaughter4['daughter1ID'].values[0], CellDF)
                gDaughters = gDaughters.append(gDaughter4)
            else:
                for uID in daughters['uID']:
                    if uID != gDaughters4['motherID'].values[0] and uID not in gDaughters['uID'].values:
                        gDaughters = gDaughters.append(find_Cell(uID, CellDF))
                        break
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


def fill_newcell(uID, CellDF):
    tmp_cell = find_cell(uID, CellDF)
    if tmp_cell.empty:
        return

    parent = find_parent(tmp_cell, CellDF)
    if not parent.empty:
        CellDF.loc[uID, 'Age'] = parent['Age'].values[0]

    if tmp_cell['daughter2ID'].values[0] != -2:
        return
    else:
        fill_newcell(tmp_cell['daughter1ID'].values[0], CellDF)
        fill_newcell(tmp_cell['daughter2ID'].values[0], CellDF)
        return


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
        CellDF.loc[uID, 'Age'] = 10
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


def cellular_ageTracking(CellDF, origin_frame=0):
    CellDF['Age'] = pd.np.nan
    for timeinLin in range(origin_frame, max(CellDF['Z'])):
        tmpDF = CellDF[CellDF['Z'] == timeinLin]
        for uID in tmpDF['uID']:
            grand_daughters = pd.DataFrame(columns=CellDF.columns.values)
            if timeinLin == 0:
                CellDF.loc[uID, 'Age'] = unk_age
            else:
                tmpcell = find_cell(uID, CellDF)
                if not tmpcell.empty:
                    parent_cell = find_parent(tmpcell, CellDF)
                    if not parent_cell.empty:
                        gParent_cell = find_parent(parent_cell, CellDF)
                        if not gParent_cell.empty:
                            grand_daughters = find_grandDaughters(gParent_cell, CellDF, t=timeinLin)
                        else:
                            grand_daughters = find_grandDaughters(parent_cell, CellDF, t=timinLin, mode="daughter")
                    else:
                        grand_daughters = find_grandDaughters(parent_cell, CellDF, t=timeinLin, mode="daughter")
            if not grand_daughters.empty:
                print grand_daughters
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
                        if np.isnan(parent_age):
                            CellDF.loc[fuID, 'Age'] = parent_age + 1
                        else:
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
                        if not parent.empty:
                            CellDF.loc[guID, 'Age'] = parent['Age'].values[0] + 1

            elif grand_daughters.shape[0] == 2:
                CellDF.loc[uID, 'Age'] = unk_age
            else:
                fill_newcell(uID, CellDF)
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
    cellular_ageTracking(cellDfWPL)


