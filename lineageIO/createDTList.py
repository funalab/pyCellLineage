#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# -*- coding: utf-8 -*-
#
# Last modified: Sat, 01 Dec 2018 15:49:00 +0900


def createDTList(cellDfWPL):
    '''
    Create a list of doubling times.

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
    D : list
        A list of the doubling times.
    '''
    DTList = list()

    for linIdx in range(max(cellDfWPL['linIdx']) + 1):
        boolArr = cellDfWPL['linIdx'] == linIdx
        DT = 0
        for cellIdx in cellDfWPL['uID'][boolArr]:
            daughter1ID = cellDfWPL['daughter1ID'][cellIdx]
            daughter2ID = cellDfWPL['daughter2ID'][cellIdx]
            DT += 1
            if daughter1ID > 0 and daughter2ID > 0:
                DTList.append(DT)
                DT = 0

    return DTList


if __name__ == "__main__":
    from .annotateLineageIdx import annotateLineageIdx
    matFilePath = ('/Users/itabashi/Research/Analysis/Schnitzcells/'
                   '9999-99-99/488/data/488_lin.mat')
    segImgsPath = ('/Users/itabashi/Research/Analysis/Schnitzcells/'
                   '9999-99-99/488/segmentation/')
    rawImgsPath = ('/Users/itabashi/Research/Experiment/microscope/'
                   '2018/08/28/ECTC_8/Pos0/forAnalysis/488FS/')
    cellDfWPL = annotateLineageIdx(matFilePath, segImgsPath, rawImgsPath)
    DTList = createDTList(cellDfWPL)
    print(DTList)
