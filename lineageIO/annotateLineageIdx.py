#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# -*- coding: utf-8 -*-
#
# Last modified: Mon, 18 Feb 2019 22:33:09 +0900
import numpy as np

from .measurePhenotypes import measurePhenotypes


def annotateLineageIdx(matFilePath, segImgsPath, rawImgsPath, originFrame=0):
    '''
    Annotate lineage indices accorting to the result of cell tracking.

    Parameters
    ----------
    matFilePath : string
                  A path to MAT files which were created by Schnitzcells
    segImgsPath : string
                  A path to directory which include segmentated images which
                  were created by Schnitzcells
    rawImgsPath : string
                  A path to direcotry which include raw images
                  which were required for Schnitzcells

    Returns
    -------
    cellDfWPL : pandas.core.frame.DataFrame
                A pandas dataframe which includes tracking result and
                phenotypes of each cell, lineage indices.
                Its name is abbreviate for cell DataFrame
                With Phenotypes, Lineage indices.
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
                - linIdx
    '''

    cellDfWP = measurePhenotypes(matFilePath,
                                 segImgsPath,
                                 rawImgsPath,
                                 originFrame)

    numOfLin = 0
    for uID in cellDfWP['uID']:
        daughter1ID = cellDfWP['daughter1ID'][uID]
        daughter2ID = cellDfWP['daughter2ID'][uID]
        if daughter1ID < 0 and daughter2ID < 0:
            numOfLin += 1

    linIdx = 0
    linList = np.zeros(len(cellDfWP['uID']))

    for uID in cellDfWP['uID']:
        motherID = cellDfWP['motherID'][uID]

        if motherID == -1:
            linList[uID] = linIdx
            linIdx += 1
        else:
            sister1ID = cellDfWP['daughter1ID'][motherID]
            sister2ID = cellDfWP['daughter2ID'][motherID]
            if sister1ID > 0 and sister2ID > 0: # 親が分裂していたら
                if sister1ID == uID:
                    linList[uID] = linList[motherID]
                else:
                    linList[uID] = linIdx
                    linIdx += 1
            else: # 親が分裂していなかったら
                linList[uID] = linList[motherID]

    linIdx = 0
    for uID in cellDfWP['uID']:
        motherID = cellDfWP['motherID'][uID]

        if motherID == -1:
            linList[uID] = linIdx
            linIdx += 1
        else:
            sister1ID = cellDfWP['daughter1ID'][motherID]
            sister2ID = cellDfWP['daughter2ID'][motherID]
            if sister1ID > 0 and sister2ID > 0: # 親が分裂していたら
                if sister1ID == uID:
                    linList[uID] = linList[motherID]
                else:
                    linList[uID] = linIdx
                    linIdx += 1
            else: # 親が分裂していなかったら
                linList[uID] = linList[motherID]


    linList = linList.astype(np.int64)
    cellDfWP['linIdx'] = linList

    return cellDfWP


if __name__ == "__main__":
    matFilePath = ('/Users/itabashi/Research/Analysis/Schnitzcells/'
                   '9999-99-99/488/data/488_lin.mat')
    segImgsPath = ('/Users/itabashi/Research/Analysis/Schnitzcells/'
                   '9999-99-99/488/segmentation/')
    rawImgsPath = ('/Users/itabashi/Research/Experiment/microscope/'
                   '2018/08/28/ECTC_8/Pos0/forAnalysis/488FS/')
    cellDfWPL = annotateLineageIdx(matFilePath, segImgsPath, rawImgsPath)
    print(cellDfWPL)
