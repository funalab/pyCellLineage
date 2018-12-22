#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# -*- coding: utf-8 -*-
#
# Last modified: Sat, 01 Dec 2018 13:47:56 +0900
import math

from calcN import calcN
from calcD import calcD


def calcL(cellDf, dt):
    '''
    Calculate an estimator Λ(t).
    Λ(t) refers the instantaneous division rate.

    Parameters
    ----------
    cellDf : pandas.core.frame.DataFrame
             A pandas DataFrame which includes tracking result.
             Column indices are like below.
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
         A time interval.

    Returns
    -------
    L : list
        A list of the instantaneous division rate.
    '''
    L = list()

    N = calcN(cellDf)
    D = calcD(cellDf, dt)

    for i in range(len(N)):
        denom = math.log(float(N[i] + D[i]) / float(N[i]))
        numer = float(dt)
        L.append(denom / numer)

    return L

if __name__ == "__main__":
    from loadSchnitz import loadSchnitz
    matFilePath = ('/Users/itabashi/Research/Analysis/Schnitzcells/'
                   '9999-99-99/488/data/488_lin.mat')
    cellDf = loadSchnitz(matFilePath)
    L = calcL(cellDf, 3)
    print(L)
