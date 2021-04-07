#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# -*- coding: utf-8 -*-
#
# Last modified: Mon, 03 Dec 2018 16:44:44 +0900
import numpy as np
import igraph


def createGraph(cellDf, attr=None):
    '''
    Create a graph of adjacency matrix.

    Parameters
    ----------
    cellDf : pandas.core.frame.DataFrame
    attr : string

    Returns
    -------
    graph : igraph.Graph
    adjMat : numpy.ndarray
    '''
    graph = igraph.Graph()
    graph.add_vertices(len(cellDf))

    for i in range(len(cellDf)):
        if cellDf['daughter1ID'][i] > 0:
            graph.add_edge(cellDf['uID'][i], cellDf['daughter1ID'][i])
        if cellDf['daughter2ID'][i] > 0:
            graph.add_edge(cellDf['uID'][i], cellDf['daughter2ID'][i])

    adjMat = np.array(list(graph.get_adjacency()))

    if attr is not None:
        graph[attr] = cellDf[attr]

    return graph, adjMat


if __name__ == "__main__":
    from .loadSchnitz import loadSchnitz
    matFilePath = ('/Users/itabashi/Research/Analysis/Schnitzcells/'
                   '9999-99-99/488/data/488_lin.mat')
    cellDf = loadSchnitz(matFilePath)
    graph, adjMat = createGraph(cellDf)
    np.savetxt('cG.csv', adjMat, fmt='%d', delimiter=',')
