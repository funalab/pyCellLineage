#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# -*- coding: utf-8 -*-
#
# Last modified: Sun, 03 Feb 2019 14:27:40 +0900
import numpy as np
import pandas as pd
from skimage import measure
from skimage import morphology

from loadSchnitz import loadSchnitz
from loadMatImgs import loadMatImgs
from loadRawImgs import loadRawImgs
from extractIntensity import extractIntensity
from extractArea import extractArea

def atp(intens, atp_path):
    atp = list()
    atp_df = pd.read_csv(atp_path)
    emax = float(atp_df[atp_df['parameter'] == 'Emax']['value'])
    d = float(atp_df[atp_df['parameter'] == 'd']['value'])
    EC50 = float(atp_df[atp_df['parameter'] == 'EC50']['value'])
    for inten in intens:
        if float(inten) < d:
            atp.append(0)
        elif float(inten) > emax:
            atp.append(((emax-d)/emax*((EC50)**2))/(1-((emax-d)/emax))**0.5)
        else:
            atp.append((((float(inten)-d)/emax*((EC50)**2))/(1-((float(inten)-d)/emax)))**0.5)
    return atp

def measurePhenotypes(matFilePath, segImgsPath, rawImgsPath, originFrame=0,atp_path="~/git/pyLineage/lineageIO/atp_calib.csv"):
    '''
    Measure phenotypes(such as cell area, fluorescence intensity) of each cell.

    Parameters
    ----------
    matFilePath : A path to MAT files which were created by Schnitzcells
    segImgsPath : A path to directory which include segmentated images which
                  were created by Schnitzcells
    rawImgsPath : A path to directory which include raw images
                  which were required for Schnitzcells
    originFrame : numeric
                  An index of origin frame.

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
               Mean fluorescent intensity of each cell
               - area
    '''
    cellDf = loadSchnitz(matFilePath)
    segImgsList = loadMatImgs(segImgsPath)
    rawImgsList = loadRawImgs(rawImgsPath)

    areaList = list()
    intensityList = list()
    cellDfWP = cellDf.copy()
    # for frameIdx in range(len(segImgsList)):
    #     cellIndices = np.unique(segImgsList[frameIdx])
    #     cellIndices = np.delete(cellIndices, 0)  # Ignore background
    #     areaList.append(extractArea(segImgsList[frameIdx],
    #                                 rawImgsList[frameIdx]))
    #     intensityList.append(extractIntensity(segImgsList[frameIdx],
    #                                           rawImgsList[frameIdx]))
    for frameIdx in range(originFrame,len(segImgsList)):
        cellIndices = np.unique(segImgsList[frameIdx])
        cellIndices = np.delete(cellIndices, 0)  # Ignore background
        areaList.append(extractArea(segImgsList[frameIdx]))
        intensityList.append(extractIntensity(segImgsList[frameIdx],
                                              rawImgsList[frameIdx]))

    area = list()
    intens = list()
    for cellIdx in range(len(cellDf)):
        timePoint = cellDf['Z'][cellIdx] - originFrame
        cellNo = cellDf['cellNo'][cellIdx]
        area.append(areaList[timePoint][cellNo])
        intens.append(intensityList[timePoint][cellNo])

    cellDfWP['intensity'] = intens
    cellDfWP['area'] = area  # [pixel ^ 2]
    # celDfWPhenotypes['area'] = area * 0.065 ** 2 [um ^ 2]

    # add ATP column
    cellDfWP['ATP'] = atp(intens,atp_path)
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
