#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# -*- coding: utf-8 -*-
#
# Last modified: Thu, 31 Jan 2019 08:16:47 +0900
import numpy as np

from .annotateLineageIdx import annotateLineageIdx
from .loadMatImgs import loadMatImgs
from .createUniqueColorList import createUniqueColorList


def visualizeTrackedCells(matFilePath, segImgsPath, rawImgsPath, originFrame=0):
    '''
    visualizeTrackedCells

    Parameters
    ----------
    matFilePath : A path to mat file which was outputed by Schnitzcells
    segImgsPath : A path to directory which include segmentated images which
                  were outputed by Schnitzcells
    rawImgsPath : A path to direcotry which include raw images which
                  were required by Schintzcells

    Returns
    -------------
    trackedImgs : A list of numpy arrays.
                  Each array corresponds to the segmentated
                  image labeld with lineage index.
    '''

    cellDfWPL = annotateLineageIdx(matFilePath= matFilePath, segImgsPath=segImgsPath, rawImgsPath=rawImgsPath, originFrame=originFrame)
    uColList = createUniqueColorList(np.max(cellDfWPL['linIdx'] + 1))

    segImgs = loadMatImgs(segImgsPath)
    imgX, imgY = segImgs[0].shape
    trackedImgs = [np.zeros((imgX, imgY, 3), dtype=np.uint8)
                   for i in range(len(segImgs))]

    cellDfWPL.sort_values(['Z', 'cellNo'])

    for time in range(len(segImgs)):
        print((time + 1))
        timeSpecifiedDf = cellDfWPL[cellDfWPL['Z'] == time + 1]
        boolArrtmp = cellDfWPL['Z'] == time + 1
        if boolArrtmp.any():
            for cellIdx in range(1, max(timeSpecifiedDf['cellNo']) + 2):
            # for cellIdx in timeSpecifiedDf['cellNo']:
                boolArr = timeSpecifiedDf['cellNo'] == cellIdx - 1
                # boolArr = timeSpecifiedDf['cellNo'] == cellIdx + 1
                if boolArr.any():
                    linIdxDf = timeSpecifiedDf[boolArr]
                    isolatedCellIdx = np.where(segImgs[time] == cellIdx)
                    color = np.array(uColList[linIdxDf['linIdx'].values[0]]) * 255
                    trackedImgs[time][isolatedCellIdx] = color

    return trackedImgs


if __name__ == "__main__":
    matFilePath = ('/Users/itabashi/Research/Analysis/Schnitzcells/'
                   '9999-99-99/488/data/488_lin.mat')
    segImgsPath = ('/Users/itabashi/Research/Analysis/Schnitzcells/'
                   '9999-99-99/488/segmentation/')
    rawImgsPath = ('/Users/itabashi/Research/Experiment/microscope/'
                   '2018/08/28/ECTC_8/Pos0/forAnalysis/488FS/')
    imgs = visualizeTrackedCells(matFilePath, segImgsPath, rawImgsPath)
