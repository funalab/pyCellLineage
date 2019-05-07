#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# -*- coding: utf-8 -*-
#
# Last modified: Fri, 30 Nov 2018 22:20:53 +0900


def calcD(cellDf, dt):
    '''
    Calculate an estimator D(t).
    D(t) refers to the number of cells that divided t and dt.

    Parameters
    ----------
    cellDf : pandas.core.frame.DataFrame
             A pandas DataFrame which includes tracking result.
             Column indices are like below
             - ID
             - uID
             - motherID
             - daughter1ID
             - daughter2ID
             - cenX
             - cenY
             - Z
             - cellNo
             ...
    dt : numeric
         A time interval

    Returns
    -------
    D : list
        A list of the numbers of cells that divided between t and dt.
    '''
    D = list()

    justDivided = list()
    for i in range(len(cellDf)):
        motherID = cellDf['motherID'][i]

        if motherID == -1:
            justDivided.append(False)
        elif (cellDf['daughter1ID'][motherID] > 0 and
              cellDf['daughter2ID'][motherID] > 0):
            justDivided.append(True)
        else:
            justDivided.append(False)

    justDividedCells = cellDf[justDivided]
    for t in range(max(cellDf['Z'])):
        tmp = 0
        for i in range(t, t + dt):
            if i in justDividedCells['Z'].values:
                tmp += len(justDividedCells[justDividedCells['Z'] == i])
        D.append(int(tmp / 2))

    return D


if __name__ == "__main__":
    from loadSchnitz import loadSchnitz
    matFilePath = ('/Users/itabashi/Research/Analysis/Schnitzcells/'
                   '9999-99-99/488/data/488_lin.mat')
    cellDf = loadSchnitz(matFilePath)
    D = calcD(cellDf, 3)
    print(D)
