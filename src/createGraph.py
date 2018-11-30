#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# -*- coding: utf-8 -*-
#
# Last modified: Fri, 30 Nov 2018 17:43:04 +0900
import networkx as nx


def createGraph(cellDf):
    graph = nx.DiGraph()
    graph.add_nodes_from(cellDf['uID'])
    for i in range(len(cellDf['uID'])):
        if cellDf['daughter1ID'][i] > 0:
            graph.add_edge(cellDf['uID'][i], cellDf['daughter1ID'][i])
        if cellDf['daughter2ID'][i] > 0:
            graph.add_edge(cellDf['uID'][i], cellDf['daughter2ID'][i])

    return graph


if __name__ == "__main__":
    from loadSchnitz import loadSchnitz

    matFilePath = ('/Users/itabashi/Research/Analysis/Schnitzcells/'
                   '9999-99-99/488/data/488_lin.mat')
    cellDf = loadSchnitz(matFilePath)
    graph = createGraph(cellDf)
    print(type(graph))
