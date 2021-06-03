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
                    attrMax=0, attrMin=0, ylim=None,show=False,
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
    for i in range(len(cellDfWP)):
        motherID = cellDfWP['motherID'][i]
        Z = cellDfWP['Z'][i]
        if motherID == -1 and Z == 0:
            rootIdx.append(i)

    if attr is not None:
        unique_attr = list(set(cellDfWP[attr]))
        if type(unique_attr[1])==str :
            conv_attr = "conv_" + str(attr)
            cnt = 0
            total_dict = dict()
            legend = dict()
            for unique in unique_attr:
                print(unique)
                uid_list = list(cellDfWP[cellDfWP[attr] == unique]['uID'])
                total_dict.update(list(zip(uid_list,np.repeat(cnt,len(uid_list)))))
                cnt = cnt + 1
                legend.update({unique:cnt})
            print(total_dict)
            cellDfWP[conv_attr]=list(total_dict.values())
            if savePath is not None:
                df = pd.DataFrame.from_dict(legend, orient="index")
                df.to_csv(os.path.join(savePath,"legend.csv"))
            else:
                print(legend)
                print(cellDfWP)
            attr = conv_attr

        if attrMax is None:
            maxAttr = float(max(cellDfWP[attr]))
        else:
            maxAttr = attrMax

        if attrMin is None:
            minAttr = float(min(cellDfWP[attr]))
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
