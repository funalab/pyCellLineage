"""
Author: Joel Nakatani
Overview:

Parameters:
"""

from .calcEL import constructTimeRef
import math


def GeneralizedEL(timeRef, lam, linCutOff, lin_gel=20):
    nlin = len(timeRef)
    tot = nlin * (linCutOff - lin_gel + 1)
    ret = 0.0

    for i in range(nlin):
        for j in range(linCutOff - lin_gel + 1):
            ret_com = 1.0

            if len(timeRef[i]) > (j + lin_gel - 1):  # index error without -1
                for k in range(lin_gel):
                    ret_com = ret_com * math.exp(-lam * timeRef[i][j + k])
                ret += ret_com
    # print(ret/float(tot))

    if ret / float(tot) == 0:
        return None

    return math.log(ret / float(tot)) / lin_gel


def CalcGEL(CellDF, timeRef=None, err=0.00001, linCutOff=69, lin_gel=20):
    if timeRef == None:
        timeRef = constructTimeRef(CellDF)
    lambda_min = 0.0
    lambda_max = 1.0

    while (lambda_max - lambda_min) / (lambda_max + lambda_min) > err:
        lam = 0.5 * (lambda_max + lambda_min)
        gelVal = GeneralizedEL(timeRef, lam, linCutOff, lin_gel=lin_gel)

        if gelVal == None:
            return None
        else:
            if gelVal > -math.log(2.0):
                lambda_min = lam
            else:
                lambda_max = lam
        # print(f'Starting Iter lamda_min:{lambda_min}')

    return lam


if __name__ == "__main__":
    import pyCellLineage.lineageIO.annotateLineageIdx as annt
    CellDF = annt.annotateLineageIdx(
        tanauchi='/Users/ryonakatani/Downloads/MC4100_37C/')
    print(CalcGEL(CellDF))
