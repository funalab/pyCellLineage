#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# -*- coding: utf-8 -*-
#
# Last modified: Tue, 19 Feb 2019 08:17:14 +0900
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import os

from .createGraph import createGraph


def cutoffMaker(CellDF,cutoff):
    CellDF = CellDF[CellDF['Z'] <= cutoff]
    CellDF.at[(CellDF['Z'] == cutoff),'daughter1ID'] = -1
    CellDF.at[(CellDF['Z'] == cutoff),'daughter2ID'] = -1
    CellDF = CellDF.reset_index()
    countup = 0
    keys = list()
    values = list()
    for uID in CellDF.uID:
        if countup != uID:
            keys.append(uID)
            values.append(countup)
        countup = countup + 1
    IDerror = list(zip(keys,values))
    print(IDerror)
    for errorID,NewID in IDerror:
        CellDF.at[(CellDF['daughter1ID'] == errorID),'daughter1ID'] = NewID
        CellDF.at[(CellDF['daughter2ID'] == errorID),'daughter2ID'] = NewID
    CellDF['uID'] = list(range(len(CellDF['uID'])))
    return CellDF
            

def create3DLineage(cellDfWP, dt=1, attr=None, savePath=None, attrMax=0,
                    attrMin=0, xlabel='x', ylabel='y', zlabel='time (hours)',
                    thetaTics=1, cmap='gnuplot', cutoff=None,
                    lim=None,degree=1
                    ):
    '''
    Draw 3D lineage.

    Parameters
    ----------
    cellDfWP : pandas.core.frame.DataFrame
               A DataFrame which function named convertionMatToDf returns.
               This DataFrame include the result of cell tracking
               Schnitzcells carried out.
    dt : numeric
         An image interval. This Parameter confluence the z axis tics
         of 3D lineage.
    attr : string
    savePath : string
               A path in which the result images will be saved.
    attrMax : numeric
    attrMin : numeric
    xlabel : string
    ylabel : string
    zlabel : string
    thetaTics : numeric
    cmap : string
    lim : list
     list with (x,y,z) coordinates

    Returns
    -------
    fig : matplotlib.figure.Figure
    '''
    plt.cla()
    plt.clf()
    if cutoff != None:
        cellDfWP = cutoffMaker(cellDfWP,cutoff)
    graph, adjMat = createGraph(cellDfWP, attr)

    if attr is not None:
        if cellDfWP.dtypes[attr] == object:
            attrStrList = sorted(cellDfWP[attr].unique(),reverse=True)
            valueDict = dict(zip(attrStrList,[i for i in range(len(attrStrList))]))
            attrIntList = list()
            for attrStr in cellDfWP[attr]:
                attrIntList.append(int(valueDict[attrStr]))

            newName = 'StrVal'
            cellDfWP[newName] = attrIntList
            attr = newName
            cmap = 'bwr'
        minPhe = float(min(cellDfWP[attr]))
        maxPhe = float(max(cellDfWP[attr]) - minPhe)
            
        if attrMax == 0 and attrMin == 0:
            if cmap== 'gnuplot':
                colors = {key: plt.cm.gnuplot((float(value) - minPhe)/maxPhe)
                          for key, value in list(cellDfWP[attr].items())}
            elif cmap == 'bwr':
                colors = {key: plt.cm.bwr((float(value) - minPhe)/maxPhe)
                          for key, value in list(cellDfWP[attr].items())}
            else:
                print("add color map to code")
                sys.exit(-1)

        else:
            if cmap == 'gnuplot':
                colors = {key: plt.cm.gnuplot((float(value) - attrMin)/(float(attrMax)-attrMin))
                          for key, value in list(cellDfWP[attr].items())}
            elif cmap == 'bwr':
                colors = {key: plt.cm.bwr((float(value) - attrMin)/(float(attrMax)-attrMin))
                      for key, value in list(cellDfWP[attr].items())}
            else:
                print("add color map to code")
                sys.exit(-1)
                

    else:
        colors = {i: (0, 0, 0)
                  for i in range(len(cellDfWP))}

    pos = {cellDfWP['uID'][i]:
           (cellDfWP['cenX'][i] - min(cellDfWP['cenX']),
            cellDfWP['cenY'][i] - min(cellDfWP['cenY']),
            cellDfWP['Z'][i] * dt)
           for i in range(len(cellDfWP))}

    fig = plt.figure(figsize=(8, 8))
    ax = Axes3D(fig,auto_add_to_figure=False)
    fig.add_axes(ax)


    for i, j in list(pos.items()):
        xi = j[0]
        yi = j[1]
        zi = j[2]
        if zi == max(cellDfWP['Z']) * dt:
            ax.scatter(xi, yi, zi, s=100,
                       color=colors[i], alpha=1, cmap=plt.cm.gnuplot)
        else:
            ax.scatter(xi, yi, zi, s=1,
                       color=colors[i], alpha=0, cmap=plt.cm.gnuplot)

    for edge in graph.es:
        source = edge.source
        target = edge.target
        x = np.array((pos[source][0], pos[target][0]))
        y = np.array((pos[source][1], pos[target][1]))
        z = np.array((pos[source][2], pos[target][2]))
        ax.plot(x, y, z, c=colors[target], lw=2, alpha=1)

    ax.zaxis.set_rotate_label(False)
    ax.set_xlabel(xlabel, fontsize=20, labelpad=18)
    ax.set_ylabel(ylabel, fontsize=20, labelpad=18)
    ax.set_zlabel(zlabel, fontsize=20, labelpad=18, rotation=90)
    ax.xaxis.set_tick_params(labelsize=12)
    ax.yaxis.set_tick_params(labelsize=12)
    ax.zaxis.set_tick_params(labelsize=12)
    if lim is not None and len(lim) == 3:
        ax.set_xlim(0,lim[0])
        ax.set_ylim(0,lim[1])
        ax.set_zlim(0,lim[2])

    if savePath is not None:
        if not os.path.isdir(savePath):
            os.mkdir(savePath)
        for angle in range(0, 360, degree):
            ax.view_init(30, angle)
            saveFile = os.path.join(savePath, str(angle)+'.tif')
            fig.savefig(saveFile, transparent=True)

    return fig


if __name__ == "__main__":
    from .measurePhenotypes import measurePhenotypes
    matFilePath = ('/Users/itabashi/Research/Analysis/Schnitzcells/'
                   '2018-08-28/488/data/488_lin.mat')
    segImgsPath = ('/Users/itabashi/Research/Analysis/Schnitzcells/'
                   '2018-08-28/488/segmentation/')
    rawImgsPath = ('/Users/itabashi/Research/Experiment/microscope/'
                   '2018/08/28/ECTC_8/Pos0/forAnalysis/488FS/')
    cellDfWP = measurePhenotypes(matFilePath, segImgsPath, rawImgsPath)
    create3DLineage(cellDfWP, 10, '/Users/itabashi/Desktop/tmp3', 'area')

