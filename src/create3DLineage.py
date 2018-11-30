#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# -*- coding: utf-8 -*-
#
# Last modified: Fri, 30 Nov 2018 19:42:54 +0900
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import os

from createGraph import createGraph


def create3DLineage(cellDfWP, dt, savePath, attribute):
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
    savePath : string
               A path in which the result images will be saved.
    attribute : string
                

    Returns
    -------

    '''
    graph = createGraph(cellDfWP)

    maxPhe = max(cellDfWP[attribute])
    colors = {key: plt.cm.gnuplot(float(value)/float(maxPhe))
              for key, value in cellDfWP[attribute].iteritems()}

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

    for i, j in enumerate(graph.edges()):
        x = np.array((pos[j[0]][0], pos[j[1]][0]))
        y = np.array((pos[j[0]][1], pos[j[1]][1]))
        z = np.array((pos[j[0]][2], pos[j[1]][2]))
        ax.plot(x, y, z, c=colors[j[1]], lw=2, alpha=1)

    ax.set_xlabel('x', fontsize=20, labelpad=18)
    ax.set_ylabel('y', fontsize=20, labelpad=18)
    ax.set_zlabel('t', fontsize=20, labelpad=18)
    ax.xaxis.set_tick_params(labelsize=12)
    ax.yaxis.set_tick_params(labelsize=12)
    ax.zaxis.set_tick_params(labelsize=12)

    for angle in range(0, 360, 1):
        ax.view_init(30, angle)
        saveFile = os.path.join(savePath, str(angle)+'.png')
        fig.savefig(saveFile, transparent=True)


if __name__ == "__main__":
    from measurePhenotypes import measurePhenotypes

    matFilePath = ('/Users/itabashi/Research/Analysis/Schnitzcells/'
                   '9999-99-99/488/data/488_lin.mat')
    segImgsPath = ('/Users/itabashi/Research/Analysis/Schnitzcells/'
                   '9999-99-99/488/segmentation/')
    rawImgsPath = ('/Users/itabashi/Research/Experiment/microscope/'
                   '2018/08/28/ECTC_8/Pos0/forAnalysis/488FS/')
    cellDfWP = measurePhenotypes(matFilePath, segImgsPath, rawImgsPath)

    create3DLineage(cellDfWP, 10, '/Users/itabashi/Desktop/tmp3', 'area')
