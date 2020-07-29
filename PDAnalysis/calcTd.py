#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# -*- coding: utf-8 -*-
#
# Last modified: Sat, 01 Dec 2018 14:21:55 +0900
import math

from .calcLp import calcLp


def calcTd(cellDf, dt):
    '''
    Calculate an estimator Td.
    Td refers the population doubling time.

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
    Td : numeric
         Population doubling time.
    '''
    Lp = calcLp(cellDf, dt)
    Td = math.log(2) / Lp
    return Td


if __name__ == "__main__":
    from loadSchnitz import loadSchnitz
    matFilePath = ('/Users/itabashi/Research/Analysis/Schnitzcells/'
                   '9999-99-99/488/data/488_lin.mat')
    cellDf = loadSchnitz(matFilePath)
    Td = calcTd(cellDf, 3)
    print(Td)
