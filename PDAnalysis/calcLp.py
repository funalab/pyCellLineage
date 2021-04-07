#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# -*- coding: utf-8 -*-
#
# Last modified: Sat, 01 Dec 2018 13:55:03 +0900
import numpy as np

from .calcL import calcL


def calcLp(cellDf, dt):
    '''
    Calculate an estimator Λp.
    Λp refers the population growth rate.

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
    Lp : numeric
         Population growth rate.
    '''
    L = calcL(cellDf, dt)
    n = len(L)
    Lp = np.sum(L[: n - 1]) / n

    return Lp


if __name__ == "__main__":
    from loadSchnitz import loadSchnitz
    matFilePath = ('/Users/itabashi/Research/Analysis/Schnitzcells/'
                   '9999-99-99/488/data/488_lin.mat')
    cellDf = loadSchnitz(matFilePath)
    Lp = calcLp(cellDf, 3)
    print(Lp)
