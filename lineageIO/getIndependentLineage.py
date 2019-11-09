#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# -*- coding: utf-8 -*-
#
# Last modified: Fri, 15 Feb 2019 17:30:02 +0900
import numpy as np
import pandas as pd
import tqdm


def getIndependentLineage(cellDfWPL):
    '''
    Get indipendent lineage

    Parameters
    ----------
    cellDfWPL : pandas.core.frame.DataFrame
                A pandas dataframe which includes tracking result and
                phenotypes of each cell, lineage indices.
    attr : str
           A string of objective attribute.

    Returns
    -------
    lineageList : list
                  A list of lineages.
    '''

    listOfLinIdx = np.unique(cellDfWPL[cellDfWPL['Z'] == np.max(cellDfWPL['Z'])]['cellNo'])
    listOfDf = list()
    missed = 0
    i = 0
    lastCellDf = cellDfWPL[cellDfWPL['Z'] == np.max(cellDfWPL['Z'])]
    for sCell_id in lastCellDf['uID']:
        sCellDf = cellDfWPL[cellDfWPL['uID']==int(sCell_id)]
        if sCellDf is not None:
            listOfDf.append(sCellDf)
            mID = int(sCellDf['motherID'])
            while mID >= 0:
                sCellDf = cellDfWPL[cellDfWPL['uID'] == mID]
                mID = int(sCellDf['motherID'])
                listOfDf[i-missed] = pd.concat([sCellDf, listOfDf[i-missed]])
        else:
            missed = missed + 1
        i = i+1           
    return listOfDf


if __name__ == "__main__":
    from annotateLineageIdx import annotateLineageIdx
    matFilePath = '/Users/itabashi/Research/Analysis/Schnitzcells/2019-01-02/488/data/488_lin.mat'
    segImgsPath = '/Users/itabashi/Research/Analysis/Schnitzcells/2019-01-02/488/segmentation/'
    rawImgsPath = '/Users/itabashi/Research/Experiment/microscope/2019/01/02/ECTC/Pos0/488'
    cellDf = annotateLineageIdx(matFilePath, segImgsPath, rawImgsPath)
    lineageList = getIndependentLineage(cellDf, 'area')
    print(lineageList)
