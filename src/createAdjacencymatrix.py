#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# -*- coding: utf-8 -*-
#
# Last modified: Fri, 30 Nov 2018 18:09:06 +0900
import numpy as np


def createAdjacencyMatrix(cellDf):
    '''
    Create an adjacency matrix

    Parameters
    ----------
    cellDf : pandas DataFrame
             
    Returns
    -------
    adjMat : list
             An adjacency matrix.
             Each node corresponds to the cell of each frame,
             and each edge corresponds to the cell division of time elapsed.
    '''
    adjMat = list()
    for i in range(len(cellDf)):
        adjMat.append(list((np.zeros(len(cellDf), dtype=int))))

    for i in range(len(cellDf)):
        if cellDf['uID'][i] != 0:
            motherID = cellDf['motherID'][i]
            selfID = cellDf['uID'][i]
            adjMat[motherID][selfID] = 1

    return adjMat


if __name__ == "__main__":
    from loadSchnitz import loadSchnitz
    matFilePath = ('/Users/itabashi/Research/Analysis/Schnitzcells/'
                   '9999-99-99/488/data/488_lin.mat')
    cellDf = loadSchnitz(matFilePath)
    adjMat = createAdjacencyMatrix(cellDf)
    print(adjMat)
