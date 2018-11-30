#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# -*- coding: utf-8 -*-
#
# Last modified: Fri, 30 Nov 2018 17:49:41 +0900
import numpy as np

from loadSchnitz import loadSchnitz
from loadMatImgs import loadMatImgs
from loadRawImgs import loadRawImgs


def measurePhenotypes(matFilePath, segImgsPath, rawImgsPath):
    '''
    Measure phenotypes(such as cell area, fluorescence intensity) of each cell.

    Parameters
    ----------
    matFilePath : A path to MAT files which were created by Schnitzcells
    segImgsPath : A path to directory which include segmentated images which
                  were created by Schnitzcells
    rawImgsPath : A path to direcotry which include raw images
                  which were required for Schnitzcells

    Returns
    -------
    cellDfWP : A pandas dataframe which includes tracking result and
               phenotypes of each cell.
               Its name is abbreviate for cell DataFrame With Phenotypes.
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
    '''
    cellDf = loadSchnitz(matFilePath)
    segImgsList = loadMatImgs(segImgsPath)
    rawImgsList = loadRawImgs(rawImgsPath)
    rawImgsList = rawImgsList[:-1]

    areaList = list()
    intensityList = list()
    cellDfWP = cellDf.copy()
    for frameIdx in range(len(segImgsList)):
        areaSubList = list()
        intensitySubList = list()
        cellIdices = np.unique(segImgsList[frameIdx])
        for cellIdx in cellIdices:
            if cellIdx != 0:  # ignore background
                boolArr = segImgsList[frameIdx] == cellIdx
                areaSubList.append(np.sum(boolArr))

                tmp = rawImgsList[frameIdx] * boolArr
                intensitySubList.append(np.sum(tmp))

        areaList.append(areaSubList)
        intensityList.append(intensitySubList)

    area = list()
    intens = list()
    for cellIdx in range(len(cellDf)):
        timePoint = cellDf['Z'][cellIdx]
        cellNo = cellDf['cellNo'][cellIdx]
        area.append(areaList[timePoint][cellNo])
        intens.append(intensityList[timePoint][cellNo])

    cellDfWP['intensity'] = [intens[i]/area[i] for i in range(len(intens))]
    cellDfWP['area'] = area  # [pixel ^ 2]
    # celDfWPhenotypes['area'] = area * 0.065 ** 2 [um ^ 2]

    return cellDfWP


if __name__ == "__main__":
    matFilePath = ('/Users/itabashi/Research/Analysis/Schnitzcells/'
                   '9999-99-99/488/data/488_lin.mat')
    segImgsPath = ('/Users/itabashi/Research/Analysis/Schnitzcells/'
                   '9999-99-99/488/segmentation/')
    rawImgsPath = ('/Users/itabashi/Research/Experiment/microscope/'
                   '2018/08/28/ECTC_8/Pos0/forAnalysis/488FS/')
    cellDfWP = measurePhenotypes(matFilePath, segImgsPath, rawImgsPath)
    print(cellDfWP)
