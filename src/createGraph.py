#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# -*- coding: utf-8 -*-
#
# Last modified: Fri, 30 Nov 2018 21:26:08 +0900
import networkx as nx


def createGraph(cellDf):
    '''
    Create a graph of adjacency matrix.

    Parameters
    ----------
    cellDf : pandas.core.frame.DataFrame

    Returns
    -------
    graph : networkx.classes.digraph.DiGraph
    adjMat : numpy.ndarray
    '''
    graph = nx.DiGraph()
    graph.add_nodes_from(cellDf['uID'])
    for i in range(len(cellDf['uID'])):
        if cellDf['daughter1ID'][i] > 0:
            # graph.add_edge(cellDf['uID'][i], cellDf['daughter1ID'][i])
            graph.add_edge(cellDf['daughter1ID'][i], cellDf['uID'][i])
        if cellDf['daughter2ID'][i] > 0:
            # graph.add_edge(cellDf['uID'][i], cellDf['daughter2ID'][i])
            graph.add_edge(cellDf['daughter2ID'][i], cellDf['uID'][i])

    adjSparseMat = nx.adjacency_matrix(graph)
    adjMat = adjSparseMat.toarray()

    return graph, adjMat


if __name__ == "__main__":
    from loadSchnitz import loadSchnitz

    matFilePath = ('/Users/itabashi/Research/Analysis/Schnitzcells/'
                   '9999-99-99/488/data/488_lin.mat')
    cellDf = loadSchnitz(matFilePath)
    graph, adjMat = createGraph(cellDf)
    import numpy as np
    np.savetxt('cG.csv', adjMat, fmt='%d', delimiter=',')
