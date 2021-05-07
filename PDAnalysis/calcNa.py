#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# -*- coding: utf-8 -*-
#
# Last modified: Sat, 01 Dec 2018 22:17:02 +0900
import numpy as np

from ..lineageIO.createDTList import createDTList


def calcNa(cellDfWPL):
    '''
    Calculate an estimator Na(τ).
    Na(τ) refers the number of cells who reach the age τ.

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

    Returns
    -------
    Na : list
         A list of the numbers of cells who reach the age τ.
    '''
    Na = list()
    maxAgeList = createDTList(cellDfWPL)

    for tau in range(np.max(maxAgeList) + 1):
        Na.append(np.sum(np.array(maxAgeList) >= tau))

    return Na


if __name__ == "__main__":
    from annotateLineageIdx import annotateLineageIdx
    matFilePath = ('/Users/itabashi/Research/Analysis/Schnitzcells/'
                   '9999-99-99/488/data/488_lin.mat')
    segImgsPath = ('/Users/itabashi/Research/Analysis/Schnitzcells/'
                   '9999-99-99/488/segmentation/')
    rawImgsPath = ('/Users/itabashi/Research/Experiment/microscope/'
                   '2018/08/28/ECTC_8/Pos0/forAnalysis/488FS/')
    cellDfWPL = annotateLineageIdx(matFilePath, segImgsPath, rawImgsPath)
    Na = calcNa(cellDfWPL)
    print(Na)
