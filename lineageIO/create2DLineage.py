#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# -*- coding: utf-8 -*-
#
# Last modified: Tue, 19 Feb 2019 13:30:12 +0900
import numpy as np
import matplotlib.pyplot as plt

from createGraph import createGraph


def create2DLineage(cellDfWP, dt=1, attr=None, savePath=None,
                    attrMax=0, attrMin=0,
                    xlabel='', ylabel='time', cmap='gnuplot'):
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
    dt : numeric
                 An interval of time lapse observation.
    attr : string
           A name of phenotype you want to express in the lineage.
           (e.g. area, intensity)
    savePath : string
               A path in which the result images will be saved.
    attrMax : numeric
    attrMin : numeric
    xlabel : string
    ylabel : string
    cmap : string

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

    if attr is not None:
        maxAttr = float(max(cellDfWP[attr]))
        minAttr = float(min(cellDfWP[attr]))
        if attrMax == 0 and attrMin == 0:
            colors = {key: plt.cm.gnuplot(
                      (float(value) - minAttr)/(float(maxAttr) - minAttr)
                      ) for key, value in cellDfWP[attr].iteritems()}
    else:
        colors = {i: (0, 0, 0)
                  for i in range(len(cellDfWP))}

    graph, adjMat = createGraph(cellDfWP, attr)
    layoutRT = graph.layout_reingold_tilford(root=rootIdx)
    pos = np.array(layoutRT.coords)
    pos[:, 1] = pos[:, 1] * dt

    ax = plt.gca()
    ax.invert_yaxis()

    for edge in graph.es:
        source = edge.source
        target = edge.target
        dx = [pos[source][0], pos[target][0]]
        dy = [pos[source][1], pos[target][1]]
        color = colors[target]
        plot = plt.plot(dx, dy, c=color)

    if savePath is not None:
        plt.savefig(savePath)

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
    create2DLineage(cellDfWPL, 10, 'area')
