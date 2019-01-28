#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# -*- coding: utf-8 -*-
#
# Last modified: Wed, 26 Dec 2018 17:31:50 +0900
import numpy as np

from createNeighborMat import createNeighborMat
from pyLineage.lineageIO.extractIntensity import extractIntensity


def randomizationTest(segImg, rawImg):
    '''
    Execute randomization test on fluorescent image of
    microcolony.

    Parameters
    ----------
    segImg : A segmented image which was created by Schnitzcells
    rawImg : A raw image which corresponds to segImgs

    Returns
    -------
    meanRatiosOfSameType : numpy.ndarray
                           A numpy.ndarray which is the result of
                           randomization test.
    '''
    neighborMat = createNeighborMat(segImg)
    intList = extractIntensity(segImg, rawImg)

    cellIndices = np.unique(segImg)
    cellIndices = np.delete(cellIndices, 0)  # Ignore background

    threshold = np.median(intList)

    typeList = list()
    for cellIdx in range(len(cellIndices)):
        if intList[cellIdx] < threshold:
            typeList.append(0)
        else:
            typeList.append(1)

    meanRatiosOfSameType = list()
    for i in range(10000):
        # Compute ratio of same type within neighboring cells.
        ratioOfSameType = list()
        for cellIdx in range(len(cellIndices)):
            numOfSameType = 0
            numOfNeighbor = np.sum(neighborMat[cellIdx])
            for neighbor in range(len(cellIndices)):
                if neighborMat[cellIdx][neighbor] == 1:
                    if typeList[cellIdx] == typeList[neighbor]:
                        numOfSameType += 1
            ratioOfSameType.append(float(numOfSameType / numOfNeighbor))
        meanRatiosOfSameType.append(np.mean(ratioOfSameType))
        intList = np.random.permutation(intList)
        typeList = list()
        for cellIdx in range(len(cellIndices)):
            if intList[cellIdx] < threshold:
                typeList.append(0)
            else:
                typeList.append(1)

    meanRatiosOfSameType = np.array(meanRatiosOfSameType)
    return meanRatiosOfSameType


if __name__ == "__main__":
    print('hoge')
