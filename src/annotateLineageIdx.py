#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# -*- coding: utf-8 -*-
#
# Last modified: Sat, 01 Dec 2018 15:21:05 +0900
from measurePhenotypes import measurePhenotypes


def annotateLineageIdx(matFilePath, segImgsPath, rawImgsPath):
    '''
    Annotate lineage indices accorting to the result of cell tracking.

    Parameters
    ----------
    matFilePath : A path to MAT files which were created by Schnitzcells
    segImgsPath : A path to directory which include segmentated images which
                  were created by Schnitzcells
    rawImgsPath : A path to direcotry which include raw images
                  which were required for Schnitzcells

    Returns
    -------
    cellDfWPL : A pandas dataframe which includes tracking result and
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

    cellDfWP = measurePhenotypes(matFilePath, segImgsPath, rawImgsPath)

    numOfLin = 0
    for uID in cellDfWP['uID']:
        daughter1ID = cellDfWP['daughter1ID'][uID]
        daughter2ID = cellDfWP['daughter2ID'][uID]
        if daughter1ID < 0 and daughter2ID < 0:
            numOfLin += 1

    linIdx = 0
    linList = list()

    for uID in cellDfWP['uID']:
        motherID = cellDfWP['motherID'][uID]

        if motherID == uID - 1 and motherID == -1:
            linList.append(linIdx)
        elif motherID != -1:
            sister1ID = cellDfWP['daughter1ID'][motherID]
            if sister1ID == uID:
                linList.append(linList[motherID])
            else:
                linIdx += 1
                linList.append(linIdx)
        else:
            linIdx += 1
            linList.append(linIdx)

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
