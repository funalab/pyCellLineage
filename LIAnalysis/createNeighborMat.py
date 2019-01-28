#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# -*- coding: utf-8 -*-
#
# Last modified: Mon, 28 Jan 2019 16:11:28 +0900
import numpy as np
from skimage import measure
from skimage import draw


def createNeighborMat(segImg):
    '''
    Create a matrix which express cell proximity.

    Parameters
    ----------
    segImgsPath : A path to directory which include segmentated images which
                  were created by Schnitzcells

    Returns
    -------
    neighborMat : numpy.ndarray
                  A matrix which express spatial neighboor of cells
                  in microcolony.
    '''
    cellIndices = np.unique(segImg)
    cellIndices = np.delete(cellIndices, 0)  # ignore background
    cellWidthList = list()
    xcArray = np.array([])
    ycArray = np.array([])
    aArray = np.array([])
    bArray = np.array([])
    thetaArray = np.array([])
    for cellIdx in cellIndices:
        img = np.where(segImg == cellIdx, cellIdx, 0)
        contour = measure.find_contours(img, 0)

        EllipseModel = measure.EllipseModel()
        EllipseModel.estimate(contour[0])
        xc, yc, a, b, theta = EllipseModel.params
        xcArray = np.append(xcArray, xc)
        ycArray = np.append(ycArray, yc)
        aArray = np.append(aArray, a)
        bArray = np.append(bArray, b)
        thetaArray = np.append(thetaArray, theta)
        # consider minor axis as cell width
        if a < b:
            cellWidthList.append(a)
        else:
            cellWidthList.append(b)

    medianCellWidth = np.median(cellWidthList)
    aArray = aArray + medianCellWidth * 3 / 4
    bArray = bArray + medianCellWidth * 3 / 4

    # exact neighborhood detection

    # simple neighborhood detection
    ellipseImgsList = list()
    for i in range(len(cellIndices)):
        xCoor, yCoor = draw.ellipse(xcArray[i],
                                    ycArray[i],
                                    aArray[i],
                                    bArray[i],
                                    rotation=thetaArray[i])
        imgShape = np.array(segImg.shape) + int(medianCellWidth) * 2
        img = np.zeros(imgShape, dtype=bool)
        xCoor = xCoor + int(medianCellWidth)
        yCoor = yCoor + int(medianCellWidth)
        img[xCoor, yCoor] = True
        ellipseImgsList.append(img)

    numOfCells = len(cellIndices)
    neighborMat = np.zeros((numOfCells, numOfCells))
    for i in range(len(cellIndices)):
        for j in range(len(cellIndices)):
            boolArr = np.logical_and(ellipseImgsList[i], ellipseImgsList[j])
            if np.any(boolArr):
                neighborMat[i][j] = 1

    return neighborMat


if __name__ == "__main__":
    segImgsPath = ('/Users/itabashi/Research/Analysis/Schnitzcells/'
                   '2018-11-10/488/segmentation/')
    rawImgsPath = ('/Users/itabashi/Research/Experiment/microscope/'
                   '2018/11/10/ECTC/488FS/')
    print(createNeighborMat(segImgsPath))
