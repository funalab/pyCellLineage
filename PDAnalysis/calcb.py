#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# -*- coding: utf-8 -*-
#
# Last modified: Sat, 01 Dec 2018 22:34:11 +0900
import math

from .calcNa import calcNa
from .calcDa import calcDa


def calcb(cellDfWPL, dt):
    '''
    Calculate an estimator b(τ).
    b(τ) refers the age-specific division rate.

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
    b : list
        A list of the age-specific division-rate.
    '''
    b = list()
    Na = calcNa(cellDfWPL)
    Da = calcDa(cellDfWPL, dt)
    for tau in range(len(Na) - 1):
        denom = math.log((float(Na[tau]) - float(Da[tau])) / float(Na[tau]))
        numer = dt
        b.append(- denom / numer)

    return b


if __name__ == "__main__":
    from annotateLineageIdx import annotateLineageIdx
    matFilePath = ('/Users/itabashi/Research/Analysis/Schnitzcells/'
                   '9999-99-99/488/data/488_lin.mat')
    segImgsPath = ('/Users/itabashi/Research/Analysis/Schnitzcells/'
                   '9999-99-99/488/segmentation/')
    rawImgsPath = ('/Users/itabashi/Research/Experiment/microscope/'
                   '2018/08/28/ECTC_8/Pos0/forAnalysis/488FS/')
    cellDfWPL = annotateLineageIdx(matFilePath, segImgsPath, rawImgsPath)
    b = calcb(cellDfWPL, 1)
    print(b)
