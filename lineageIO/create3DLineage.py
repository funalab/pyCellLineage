#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# -*- coding: utf-8 -*-
#
# Last modified: Fri, 07 Dec 2018 00:21:18 +0900
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import os

from createGraph import createGraph


def create3DLineage(cellDfWP, dt, attr=None, savePath=None):
    '''
    Draw 3D lineage.

    Parameters
    ----------
    cellDfWP : pandas DataFrame
               A DataFrame which function named convertionMatToDf returns.
               This DataFrame include the result of cell tracking
               Schnitzcells carried out.
    dt : numeric
         An image interval. This Parameter confluence the z axis tics
         of 3D lineage.
    attr : string
    savePath : string
               A path in which the result images will be saved.

    Returns
    -------
    fig : matplotlib.figure.Figure
    '''
    graph, adjMat = createGraph(cellDfWP, attr)

    if attr is not None:
        maxPhe = max(cellDfWP[attr])
        colors = {key: plt.cm.gnuplot(float(value)/float(maxPhe))
                  for key, value in cellDfWP[attr].iteritems()}
    else:
        colors = {i: (0, 0, 0)
                  for i in range(len(cellDfWP))}

    pos = {cellDfWP['uID'][i]:
           (cellDfWP['cenX'][i] - min(cellDfWP['cenX']),
            cellDfWP['cenY'][i] - min(cellDfWP['cenY']),
            cellDfWP['Z'][i] * dt)
           for i in range(len(cellDfWP))}

    fig = plt.figure(figsize=(8, 8))
    ax = Axes3D(fig)

    for i, j in pos.iteritems():
        xi = j[0]
        yi = j[1]
        zi = j[2]
        if zi == max(cellDfWP['Z']) * dt:
            ax.scatter(xi, yi, zi, s=100,
                       c=colors[i], alpha=1, cmap=plt.cm.gnuplot)
        else:
            ax.scatter(xi, yi, zi, s=1,
                       c=colors[i], alpha=0, cmap=plt.cm.gnuplot)

    for edge in graph.es:
        source = edge.source
        target = edge.target
        x = np.array((pos[source][0], pos[target][0]))
        y = np.array((pos[source][1], pos[target][1]))
        z = np.array((pos[source][2], pos[target][2]))
        ax.plot(x, y, z, c=colors[target], lw=2, alpha=1)

    ax.set_xlabel('x', fontsize=20, labelpad=18)
    ax.set_ylabel('y', fontsize=20, labelpad=18)
    ax.set_zlabel('t', fontsize=20, labelpad=18)
    ax.xaxis.set_tick_params(labelsize=12)
    ax.yaxis.set_tick_params(labelsize=12)
    ax.zaxis.set_tick_params(labelsize=12)

    if savePath is not None:
        for angle in range(0, 360, 1):
            ax.view_init(30, angle)
            saveFile = os.path.join(savePath, str(angle)+'.tif')
            fig.savefig(saveFile, transparent=True)

    return fig


if __name__ == "__main__":
    from measurePhenotypes import measurePhenotypes
    matFilePath = ('/Users/itabashi/Research/Analysis/Schnitzcells/'
                   '2018-08-28/488/data/488_lin.mat')
    segImgsPath = ('/Users/itabashi/Research/Analysis/Schnitzcells/'
                   '2018-08-28/488/segmentation/')
    rawImgsPath = ('/Users/itabashi/Research/Experiment/microscope/'
                   '2018/08/28/ECTC_8/Pos0/forAnalysis/488FS/')
    cellDfWP = measurePhenotypes(matFilePath, segImgsPath, rawImgsPath)
    create3DLineage(cellDfWP, 10, '/Users/itabashi/Desktop/tmp3', 'area')
