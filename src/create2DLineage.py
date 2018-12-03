#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# -*- coding: utf-8 -*-
#
# Last modified: Mon, 03 Dec 2018 16:21:13 +0900
import numpy as np
import matplotlib.pyplot as plt

from createGraph import createGraph


def create2DLineage(cellDfWP, attribute):
    '''
    Draw 2D lineage.

    Parameters
    ----------
    cellDfWPL : pandas.core.frame.DataFrame
                A pandas DataFrame which includes tracking result and
                phenotypes.
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
                - area
                ...
    attribute : string
                A name of phenotype you want to express in the lineage.

    Returns
    -------
    plot : list
           A list of matplotlib.lines.Line2D.
    '''
    rootIdx = list()
    for i in range(len(cellDfWP)):
        motherID = cellDfWP['motherID'][i]
        if motherID == -1:
            rootIdx.append(i)

    graph, adjMat = createGraph(cellDfWPL)
    layoutRT = graph.layout_reingold_tilford(root=rootIdx)
    pos = np.array(layoutRT.coords)

    pos[:, 1] = -pos[:, 1]

    for edge in graph.es:
        source = edge.source
        target = edge.target
        dx = [pos[source][0], pos[target][0]]
        dy = [pos[source][1], pos[target][1]]
        plot = plt.plot(dx, dy)

    plt.show()

    return plot


if __name__ == "__main__":
    from annotateLineageIdx import annotateLineageIdx
    matFilePath = ('/Users/itabashi/Research/Analysis/Schnitzcells/'
                   '9999-99-99/488/data/488_lin.mat')
    segImgsPath = ('/Users/itabashi/Research/Analysis/Schnitzcells/'
                   '9999-99-99/488/segmentation/')
    rawImgsPath = ('/Users/itabashi/Research/Experiment/microscope/'
                   '2018/08/28/ECTC_8/Pos0/forAnalysis/488FS/')
    cellDfWPL = annotateLineageIdx(matFilePath, segImgsPath, rawImgsPath)
    create2DLineage(cellDfWPL, 'hoge')
