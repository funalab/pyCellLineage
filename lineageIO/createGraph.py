#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# -*- coding: utf-8 -*-
#
# Last modified: Fri, 14 Oct 2022 02:24:03 +0900
import numpy as np
import igraph


def createGraph(cellDf, attr=None):
    """
    Create a graph of adjacency matrix.

    Parameters
    ----------
    cellDf : pandas.core.frame.DataFrame
    attr : string

    Returns
    -------
    graph : igraph.Graph
    adjMat : numpy.ndarray
    """
    graph = igraph.Graph()
    graph.add_vertices(len(cellDf))
    uIDs = list(cellDf["uID"])
    uID2vertID = dict(zip(uIDs, list(range(len(uIDs)))))
    fakeCells = 0

    for i in range(len(cellDf)):
        if cellDf["daughter1ID"][i] > 0:
            graph.add_edge(
                uID2vertID[cellDf["uID"][i]], uID2vertID[cellDf["daughter1ID"][i]]
            )
        # elif cellDf['daughter1ID'][i] == -1:
        #     # create fake cell for abrupt ends(removed from ROI
        #     graph.add_vertices(1)
        #     graph.add_edge(cellDf['uID'][i], fakeCells + len(cellDf))
        #     fakeCells += 1

        if cellDf["daughter2ID"][i] > 0:
            graph.add_edge(
                uID2vertID[cellDf["uID"][i]], uID2vertID[cellDf["daughter2ID"][i]]
            )
        elif cellDf["daughter2ID"][i] == -3:
            # create fake cell for cell removed from ROI
            graph.add_vertices(1)
            graph.add_edge(uID2vertID[cellDf["uID"][i]], fakeCells + len(cellDf))
            fakeCells += 1

    adjMat = np.array(list(graph.get_adjacency()))

    if attr is not None:
        graph[attr] = cellDf[attr]

    return graph, adjMat


if __name__ == "__main__":
    from .loadSchnitz import loadSchnitz

    matFilePath = (
        "/Users/itabashi/Research/Analysis/Schnitzcells/"
        "9999-99-99/488/data/488_lin.mat"
    )
    cellDf = loadSchnitz(matFilePath)
    graph, adjMat = createGraph(cellDf)
    np.savetxt("cG.csv", adjMat, fmt="%d", delimiter=",")
