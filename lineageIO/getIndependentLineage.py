#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# -*- coding: utf-8 -*-
#
# Last modified: Mon, 28 Jan 2019 19:16:23 +0900
import numpy as np


def getIndependentLineage(cellDfWPL, attr='area'):
    '''
    Get indipendent lineage

    Parameters
    ----------
    cellDfWPL : pandas.core.frame.DataFrame
                A pandas dataframe which includes tracking result and
                phenotypes of each cell, lineage indices.
    area : str
           A string of objective attribute.

    Returns
    -------
    lineageList : list
                  A list of lineages.
    '''

    numOfLin = np.max(cellDfWPL['linIdx']) + 1
    numOfT = np.max()
    lineageList = list()

    for i in range(numOfLin + 1):
        sCellDf = cellDfWPL[cellDfWPL['linIdx'] == i]
        motherCellList = list(sCellDf['motherID'])
        motherID = motherCellList[0]
        mLinIdx = cellDfWPL[cellDfWPL['uID'] == motherID]['linIdx']
        mCellDf = cellDfWPL[cellDfWPL['linIdx'] == mLinIdx]


if __name__ == "__main__":
    main()

