#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# -*- coding: utf-8 -*-
#
# Last modified: Wed, 26 Dec 2018 00:08:25 +0900
import numpy as np
from skimage import measure
from skimage import morphology

from loadSchnitz import loadSchnitz
from loadMatImgs import loadMatImgs
from loadRawImgs import loadRawImgs
from extractIntensity import extractIntensity
from extractArea import extractArea


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

    areaList = list()
    intensityList = list()
    cellDfWP = cellDf.copy()
    for frameIdx in range(len(segImgsList)):
        cellIndices = np.unique(segImgsList[frameIdx])
        cellIndices = np.delete(cellIndices, 0)  # Ignore background

        areaList.append(extractArea(segImgsList[frameIdx],
                                    rawImgsList[frameIdx]))
        intensityList.append(extractIntensity(segImgsList[frameIdx],
                                              rawImgsList[frameIdx]))

    area = list()
    intens = list()
    for cellIdx in range(len(cellDf)):
        timePoint = cellDf['Z'][cellIdx] - 1
        cellNo = cellDf['cellNo'][cellIdx]
        area.append(areaList[timePoint][cellNo])
        intens.append(intensityList[timePoint][cellNo])

    cellDfWP['intensity'] = intens
    cellDfWP['area'] = area  # [pixel ^ 2]
    # celDfWPhenotypes['area'] = area * 0.065 ** 2 [um ^ 2]

    return cellDfWP


if __name__ == "__main__":
    matFilePath = ('/Users/itabashi/Research/Analysis/Schnitzcells/'
                   '2018-11-10/488/data/488_lin.mat')
    segImgsPath = ('/Users/itabashi/Research/Analysis/Schnitzcells/'
                   '2018-11-10/488/segmentation/')
    rawImgsPath = ('/Users/itabashi/Research/Experiment/microscope/'
                   '2018/11/10/ECTC/488FS/')
    cellDfWP = measurePhenotypes(matFilePath, segImgsPath, rawImgsPath)
    print(cellDfWP)
