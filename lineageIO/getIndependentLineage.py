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

    for i in tqdm.tqdm(range(len(listOfLinIdx))):
        sCellDf = cellDfWPL[cellDfWPL['Z'] == np.max(cellDfWPL['Z'])][cellDfWPL['linIdx'] == i]
        listOfDf.append(sCellDf)
        mID = int(sCellDf['motherID'])
        while mID >= 0:
            sCellDf = cellDfWPL[cellDfWPL['uID'] == mID]
            mID = int(sCellDf['motherID'])
            listOfDf[i] = pd.concat([sCellDf, listOfDf[i]])

    return listOfDf


if __name__ == "__main__":
    from annotateLineageIdx import annotateLineageIdx
    matFilePath = '/Users/itabashi/Research/Analysis/Schnitzcells/2019-01-02/488/data/488_lin.mat'
    segImgsPath = '/Users/itabashi/Research/Analysis/Schnitzcells/2019-01-02/488/segmentation/'
    rawImgsPath = '/Users/itabashi/Research/Experiment/microscope/2019/01/02/ECTC/Pos0/488'
    cellDf = annotateLineageIdx(matFilePath, segImgsPath, rawImgsPath)
    lineageList = getIndependentLineage(cellDf, 'area')
    print(lineageList)
