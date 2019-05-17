#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# -*- coding: utf-8 -*-
#
# Last modified: Fri, 30 Nov 2018 21:57:42 +0900
import numpy as np


def calcN(cellDf):
    '''
    Calculate an estimator N(t).
    N(t) refers the number of cells at the time.

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

    Returns
    -------
    N : list
        A list of the cell numbers at each time.
    '''
    N = list()

    for i in range(np.min(cellDf['Z']), np.max(cellDf['Z'])+1):
        existingCell = cellDf[cellDf['Z'] == i]
        N.append(len(existingCell))

    return N


if __name__ == "__main__":
    from loadSchnitz import loadSchnitz
    matFilePath = ('/Users/itabashi/Research/Analysis/Schnitzcells/'
                   '9999-99-99/488/data/488_lin.mat')
    cellDf = loadSchnitz(matFilePath)
    N = calcN(cellDf)
    print(N)
