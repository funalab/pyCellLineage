#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# -*- coding: utf-8 -*-
#
# Last modified: Tue, 25 Dec 2018 22:43:08 +0900
import numpy as np
from skimage import measure
from skimage import morphology


def extractIntensity(segImg, rawImg):
    '''
    Extract intensitiy of each cell.

    Parameters
    ----------
    segImg : numpy.ndarray
             A segmented image whch include cell masks.
    rawImg : numpy.ndarray
             A raw image corresponds to segImg.

    Returns
    -------
    meanIntList : float
                  A list of mean intensity calculated over the central
                  area of each cell.
    '''
    cellWidthList = list()

    cellIndices = np.unique(segImg)
    cellIndices = np.delete(cellIndices, 0)  # Ignore background
    for cellIdx in cellIndices:
        binaryCellMask = segImg == cellIdx
        contour = measure.find_contours(binaryCellMask, 0)
        EM = measure.EllipseModel()
        EM.estimate(contour[0])
        xc, yc, a, b, theta = EM.params
        if a < b:
            cellWidthList.append(a)
        else:
            cellWidthList.append(b)

    medianCellWidth = np.median(cellWidthList)
    erodeIter = int(medianCellWidth / 4)

    # Extract mean fluorescent intensity only over the central area of the cell
    meanIntList = list()
    for cellIdx in cellIndices:
        erodeMask = segImg == cellIdx
        for i in range(erodeIter):
            erodeMask = morphology.binary_erosion(binaryCellMask,
                                                  selem=np.ones((3, 3)))
        area = np.sum(erodeMask)
        intensity = np.sum(rawImg * erodeMask)
        meanIntList.append(intensity / area)

    return meanIntList


if __name__ == "__main__":
    from loadMatImgs import loadMatImgs
    from loadRawImgs import loadRawImgs
    segImgsPath = '/Users/itabashi/Research/Analysis/Schnitzcells/2018-11-10/488/segmentation/'
    rawImgsPath = '/Users/itabashi/Research/Experiment/microscope/2018/11/10/ECTC/488FS'
    segImgs = loadMatImgs(segImgsPath)
    rawImgs = loadRawImgs(rawImgsPath)
    meanIntList = extractIntensity(segImgs[-1], rawImgs[-1])
    print(meanIntList)
