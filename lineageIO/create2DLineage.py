#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# -*- coding: utf-8 -*-
#
# Last modified: Tue, 19 Feb 2019 13:32:52 +0900
import numpy as np
import sys
import matplotlib.pyplot as plt

from .createGraph import createGraph


def create2DLineage(cellDfWP, dt=1, attr=None, savePath=None,
                    attrMax=None, attrMin=None, ylim=None,show=False,
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
    plt.cla()
    plt.clf()
    rootIdx = list()
    uIDs = list(cellDfWP['uID'])
    uID2vertID = dict(zip(uIDs,list(range(len(uIDs)))))

    for i in range(len(cellDfWP)):
        motherID = cellDfWP['motherID'][i]
        Z = cellDfWP['Z'][i]
        if motherID == -1 or Z == min(cellDfWP['Z']):
            uID = uID2vertID[cellDfWP['uID'][i]]
            rootIdx.append(uID)
    if attr is not None:
        if cellDfWP.dtypes[attr] == object and type(cellDfWP[attr][0])==str():
            attrStrList = sorted(cellDfWP[attr].unique(),reverse=True)
            valueDict = dict(zip(attrStrList,[i for i in range(len(attrStrList))]))
            attrIntList = list()
            for attrStr in cellDfWP[attr]:
                attrIntList.append(int(valueDict[attrStr]))

            newName = 'StrVal'
            cellDfWP[newName] = attrIntList
            attr = newName
            cmap = 'bwr'
            attrMax = max(valueDict.values())
            attrMin = min(valueDict.values())

        if attrMax is None:
            maxAttr = max(cellDfWP[attr])
        else:
            maxAttr = attrMax

        if attrMin is None:
            minAttr = min(cellDfWP[attr])
        else:
            minAttr = attrMin
            
        if cmap == 'bwr':
            colors = {key: plt.cm.bwr(
                (float(value) - minAttr)/(float(maxAttr) - minAttr)
            ) for key, value in list(cellDfWP[attr].items())}

        elif cmap == 'gnuplot':
            colors = {key: plt.cm.gnuplot(
                (float(value) - minAttr)/(float(maxAttr) - minAttr)
            ) for key, value in list(cellDfWP[attr].items())}
        else:
            print("add color map to code")
            sys.exit(-1)
    else:
        colors = {i: (0, 0, 0)
                  for i in range(len(cellDfWP))}

    graph, adjMat = createGraph(cellDfWP, attr)
    layoutRT = graph.layout_reingold_tilford(root=rootIdx)
    pos = np.array(layoutRT.coords)
    pos[:, 1] = pos[:, 1] * dt

    if ylim is not None:
        plt.ylim(0,ylim)

    ax = plt.gca()
    ax.invert_yaxis()
    ax.axes.get_xaxis().set_visible(False)

    for edge in graph.es:
        source = edge.source
        target = edge.target
        dx = [pos[source][0], pos[target][0]]
        dy = [pos[source][1], pos[target][1]]
        if target not in colors.keys():
            color = (0,0,0) # Fake cells are automatically Black
        else:
            color = colors[target]
        plot = plt.plot(dx, dy, c=color)
    if savePath is not None:
        plt.savefig(savePath)
    if show:
        plt.show()

    return plot


if __name__ == "__main__":
    from .annotateLineageIdx import annotateLineageIdx
    matFilePath = ('/Users/itabashi/Research/Analysis/Schnitzcells/'
                   '9999-99-99/488/data/488_lin.mat')
    segImgsPath = ('/Users/itabashi/Research/Analysis/Schnitzcells/'
                   '9999-99-99/488/segmentation/')
    rawImgsPath = ('/Users/itabashi/Research/Experiment/microscope/'
                   '2018/08/28/ECTC_8/Pos0/forAnalysis/488FS/')
    cellDfWPL = annotateLineageIdx(matFilePath, segImgsPath, rawImgsPath)
    create2DLineage(cellDfWPL, 10, 'area')
