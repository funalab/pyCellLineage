#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# -*- coding: utf-8 -*-
#
# Last modified: Thu, 31 Jan 2019 06:05:51 +0900
import numpy as np


def extractArea(segImg, pixelSize=1.0):
    '''
    Extract area of each cell.

    Parameters
    ----------
    segImg : numpy.ndarray
             A segmented image whch include cell masks.
    pixelSize : float
                A real length of a pixel width.
                Default is set to 1.0 so that the unit of area
                would be pixel^2.

    Returns
    -------
    areaList : float
               A list of area of each cell.
    '''
    cellIndices = np.unique(segImg)
    cellIndices = np.delete(cellIndices, 0)  # Ignore background

    areaList = list()
    for cellIdx in cellIndices:
        binaryCellMask = segImg == cellIdx
        areaList.append(np.sum(binaryCellMask))

    keys = cellIndices
    values = areaList
    areaDict = dict(zip(keys, values))

    # return areaList
    return areaDict


if __name__ == "__main__":
    from loadMatImgs import loadMatImgs
    from loadRawImgs import loadRawImgs
    segImgsPath = '/Users/itabashi/Research/Analysis/Schnitzcells/2018-11-10/488/segmentation/'
    rawImgsPath = '/Users/itabashi/Research/Experiment/microscope/2018/11/10/ECTC/488FS'
    segImgs = loadMatImgs(segImgsPath)
    rawImgs = loadRawImgs(rawImgsPath)
    areaList = extractArea(segImgs[-1], rawImgs[-1])
    print(areaList)
