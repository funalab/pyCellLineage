"""
Author: Joel Nakatani
Overview:

Parameters:
"""

import math
from ..lineageIO.getIndependentLineage import getIndependentLineage


def checktimeRef(linCutOff, timeRef):
    for i in range(len(timeRef)):
        if linCutOff < len(timeRef[i]):
            return True

    return False


def EL(timeRef, lam, linCutOff):
    tot = len(timeRef) * linCutOff
    ret = 0.0

    for i in range(len(timeRef)):
        if len(timeRef[i]) >= linCutOff:
            for j in range(linCutOff):
                ret = ret + math.exp(-lam * timeRef[i][j])

    # print(ret/float(tot))

    return ret / float(tot)


def cleantimeRef(timeRef):
    tmp = list()

    for i in range(len(timeRef)):
        if len(timeRef[i]) > 0:
            tmp.append(timeRef[i])
    # print(tmp)

    return tmp


def constructTimeRef(CellDF):
    tmpDF = CellDF.copy()

    lineages = getIndependentLineage(tmpDF)
    timeRef = [[] for i in range(len(lineages))]

    for i in range(len(lineages)):
        lin = lineages[i]
        delta = 0
        dtTot = 0

        for itr in range(len(lin)):
            cell = lin.iloc[itr]

            if int(cell['daughter2ID']) == -3 or int(cell['daughter2ID']) > 0:
                if delta > 0:
                    timeRef[i].append(float(dtTot))
                delta += 1
                dtTot = 0
            dtTot += 1
        # print(f'Num of divisions:{delta}')

    # print(timeRef)

    return cleantimeRef(timeRef)


def CalcEL(CellDF, timeRef=None, err=0.00001, linCutOff=69):
    if timeRef == None:
        timeRef = constructTimeRef(CellDF)
    lambda_min = 0.0
    lambda_max = 1.0

    while ((lambda_max - lambda_min) / (lambda_max + lambda_min) > err):
        lam = 0.5 * (lambda_max + lambda_min)
        # print(f'Starting Iter lamda:{lam}')

        if EL(timeRef, lam, linCutOff) > 0.5:
            lambda_min = lam
        else:
            lambda_max = lam

        if (lambda_max + lambda_min) == 0:
            lam = None

            break

    return lam


if __name__ == "__main__":
    import pyCellLineage.lineageIO.annotateLineageIdx as annt
    CellDF = annt.annotateLineageIdx(
        tanauchi=
        '/Users/ryonakatani/LAB/labrot/BCU/lineageData/Tanauchi/MC4100_37C/')
    print(CalcEL(CellDF))
