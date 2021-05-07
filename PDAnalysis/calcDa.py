#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# -*- coding: utf-8 -*-
#
# Last modified: Sat, 01 Dec 2018 22:18:21 +0900
import numpy as np

from ..lineageIO.createDTList import createDTList


def calcDa(cellDfWPL, dt):
    '''
    Calculate an estimator Da(τ).
    Da(τ) refers the number of cells who divide between the age τ and τ + dt.

    Parameters
    ----------
    cellDfWPL : pandas.core.frame.DataFrame
                A pandas DataFrame which includes tracking result and
                lineage indices.
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
                - intensity
                - area
                - linNo
                ...
    dt : numeric
         A time interval

    Returns
    -------
    Da : list
         A list of the numbers of cells
         who divied between the age τ and τ + dt.
    '''
    Da = list()
    maxAgeList = np.array(createDTList(cellDfWPL))

    for tau in range(np.max(maxAgeList) + 1):
        bottomCond = tau <= maxAgeList
        topCond = maxAgeList < tau + dt
        boolArr = np.logical_and(bottomCond, topCond)
        Da.append(np.sum(boolArr))

    return Da


if __name__ == "__main__":
    from annotateLineageIdx import annotateLineageIdx
    matFilePath = ('/Users/itabashi/Research/Analysis/Schnitzcells/'
                   '9999-99-99/488/data/488_lin.mat')
    segImgsPath = ('/Users/itabashi/Research/Analysis/Schnitzcells/'
                   '9999-99-99/488/segmentation/')
    rawImgsPath = ('/Users/itabashi/Research/Experiment/microscope/'
                   '2018/08/28/ECTC_8/Pos0/forAnalysis/488FS/')
    cellDfWPL = annotateLineageIdx(matFilePath, segImgsPath, rawImgsPath)
    Da = calcDa(cellDfWPL, 1)
    print(Da)
