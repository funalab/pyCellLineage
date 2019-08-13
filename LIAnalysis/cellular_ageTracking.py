import pandas as pd


def find_distancePair(gDaughters, CellDF, mode="closest", originID=None):
    coordinates = list()
    for uID in gDaughters['uID']:
        tmp_cell = find_cell(uID, CellDF)
        coordinates.append((tmp_cell['uID'].values[0],tmp_cell['cenX'].values[0],tmp_cell['cenY'].values[0]))
    least_distance = (-3,-3,0)
    greatest_distance = (-3,-3,0)
    if originID is not None:
        origin_cell = find_cell(originID, CellDF)
        origin_Cellxy = (originID, origin_cell['cenX'].values[0],origin_cell['cenY'].values[0])
    for xy in coordinates:
        if originID is not None:
            distance = ((xy[1] - origin_Cellxy[1]) ** 2 + (xy[2] - origin_Cellxy[2]) ** 2) ** 0.5
            if least_distance[2] > distance:
                least_distance = (xy[0], subxy[0], distance)
            if greatest_distance[2] < distance:
                greatest_distance = (xy[0], subxy[0], distance)
        else:
            subcoordinates = np.setdiff1d(coordinates,xy)
            for subxy in subcoordinates:
                distance = ((xy[1] - subcoordinates[1]) ** 2 + (xy[2] - subcoordinates[2]) ** 2) ** 0.5
                if least_distance[2] > distance:
                    least_distance = (xy[0], subxy[0], distance)
                if greatest_distance[2] < distance:
                    greatest_distance = (xy[0], subxy[0], distance)

    if mode == "closest":
        cDaughters.loc[cDaughter1['uID'].values[0]] = find_cell(least_distance[0],CellDF)
        cDaughters.loc[cDaughter2['uID'].values[0]] = find_cell(least_distance[1], CellDF)
        return cDaughters
    if mode == "farthest":
        fDaughters.loc[uID] = find_cell(greatest_distance[0], CellDF)
        fDaughters.loc[uID] = find_cell(greatest_distance[1], CellDF)
        return fDaughters


def find_cell(uID, CellDF):
    return CellDF[CellDF['uID'] == uID]


def find_grandDaughters(cell_slice, CellDF, t=None):
    daughter_cell1 = find_Cell(cell_slice['daughter1ID'], CellDF)
    daughter_cell2 = find_Cell(cell_slice['daughter2ID'], CellDF)
    gDaughter1 = find_Cell(daughter_cell1['daughter1ID'], CellDF)
    gDaughter2 = find_Cell(daughter_cell1['daughter2ID'], CellDF)
    gDaughter3 = find_Cell(daughter_cell2['daughter1ID'], CellDF)
    gDaughter4 = find_Cell(daughter_cell2['daughter2ID'], CellDF)

    if t is None:
        gDaughters.loc[gDaughter1['uID'].values[0]] = gDaughter1
        gDaughters.loc[gDaughter2['uID'].values[0]] = gDaughter2
        gDaughters.loc[gDaughter3['uID'].values[0]] = gDaughter3
        gDaughters.loc[gDaughter4['uID'].values[0]] = gDaughter4
    else:
        if gDaughter1['Z'] == t:
            gDaughters.loc[gDaughter1['uID'].values[0]] = gDaughter1
        if gDaughter2['Z'] == t:
            gDaughters.loc[gDaughter2['uID'].values[0]] = gDaughter2
        if gDaughter3['Z'] == t:
            gDaughters.loc[gDaughter3['uID'].values[0]] = gDaughter3
        if gDaughter4['Z'] == t:
            gDaughters.loc[gDaughter4['uID'].values[0]] = gDaughter4
    return gDaughters


def find_parent(cell_slice, CellDF):
    uID = cell_slice['motherID'].values[0]
    parent = CellDF[CellDF['uID'] == uID]
    return parent


def cellular_ageTracking(CellDF):
    CellDF['Age'] = Nan
    for timeinLin in range(max(CellDF['Z'])):
        tmpDF = CellDF[CellDF['Z'] == timeinLin]
        if timeinLin == 0:
            for uID in tmpDF['uID']:
                tmpCell = find_cell(uID, CellDF)
                CellDF.loc[uID, 'Age'] = -1  # No Distinct age
                DaughterID = tmpCell['daughter1ID'].values[0]
                DaughterID2 = tmpCell['daughter2ID'].values[0]
                gDaughters = find_grandDaughters(tmpCell, CellDF)
                cDaughters = find_distancePair(gDaughters, CellDF)
                for cuID in cDaughters:
                    CellDF.loc[cuID, 'Age'] = 1
        else:
            undecided_cells = tmpDF[tmpDF['Age'] == Nan]
            if len(undecided_cells) != 0:
                for uID in undecided_cells['uID']:
                    tmpcell = find_Cell(uID, CellDF)
                    parent_cell = find_parent(tmpcell, CellDF)
                    gParent_cell = find_parent(parent_cell, CellDF)
                    grand_daughters = find_grandDaughters(gParent_cell, CellDF, t=timeinLin)
                    if not None in grand_daughters:
                        closest_pair = find_distancePair(grand_daughters, CellDF)
                        farthest_pair = find_distancePair(grand_daughters, CellDF, mode="farthest")
                        # add check if no overlaps later
                        for cuID in closest_pair['uID']:
                            CellDF.loc[cuID, 'Age'] = 1
                        for fuID in farthest_pair['uID']:
                            cell = CellDF[CellDF['uID'] == fuID]
                            parent = find_parent(cell)
                            parent_age = parent['Age'].values[0]
                            if parent_age != Nan:
                                CellDF.loc[fuID, 'Age'] = parent_age + 1
                            else:
                                CellDF.loc[fuID,'Age'] = Nan
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

        undecided_cells = tmpDF[tmpDF['Age'] == Nan]  # fill ages for unchanging cells
        for uID in undecided_cells['uID']:
            tmp_cell = find_cell(uID, CellDF)
            while tmp_cell['daughter1ID'].values[0] == -2 or tmp_cell['daughter2ID'].values[0] == -2:
                tmp_cell = find_parent(tmp_cell, CellDF)
            CellDF.loc[uID, 'Age'] = tmp_cell['Age'].values[0]


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


