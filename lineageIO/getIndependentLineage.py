#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# -*- coding: utf-8 -*-
#
# Last modified: Fri, 14 Oct 2022 02:24:32 +0900
import numpy as np
import pandas as pd
from tqdm import tqdm
import multiprocessing as mp


def backTrack(cellDfWPL, sCell_id):
    sCellDf = cellDfWPL[cellDfWPL["uID"] == int(sCell_id)]
    if sCellDf is not None:
        tmpDf = sCellDf.copy()
        mID = int(sCellDf["motherID"])
        while mID >= 0:
            sCellDf = cellDfWPL[cellDfWPL["uID"] == mID]
            mID = int(sCellDf["motherID"])
            tmpDf = pd.concat([sCellDf, tmpDf])
    return tmpDf


def getIndependentLineage(cellDfWPL, mode=None):
    """
    Get indipendent lineage

    Parameters
    ----------
    cellDfWPL : pandas.core.frame.DataFrame
                A pandas dataframe which includes tracking result and
                phenotypes of each cell, lineage indices.
    attr : str
           A string of objective attribute.

    Returns
    -------
    lineageList : list
                  A list of lineages.
    """

    if mode is None:
        listOfLinIdx = np.unique(
            cellDfWPL[cellDfWPL["Z"] == np.max(cellDfWPL["Z"])]["cellNo"]
        )
        listOfDf = list()
        missed = 0
        i = 0
        lastCellDf = cellDfWPL[
            (cellDfWPL["daughter1ID"] < 0) & (cellDfWPL["Z"] > np.min(cellDfWPL["Z"]))
        ]
        for sCell_id in tqdm(lastCellDf["uID"]):
            sCellDf = cellDfWPL[cellDfWPL["uID"] == int(sCell_id)]
            if sCellDf is not None:
                listOfDf.append(sCellDf)
                mID = int(sCellDf["motherID"])
                while mID >= 0:
                    sCellDf = cellDfWPL[cellDfWPL["uID"] == mID]
                    mID = int(sCellDf["motherID"])
                    listOfDf[i - missed] = pd.concat([sCellDf, listOfDf[i - missed]])
            else:
                missed = missed + 1
            i = i + 1
    if mode == "parallel":
        threads = 4
        listOfLinIdx = np.unique(
            cellDfWPL[cellDfWPL["Z"] == np.max(cellDfWPL["Z"])]["cellNo"]
        )
        listOfDf = list()
        missed = 0
        lastCellDf = cellDfWPL[
            (cellDfWPL["daughter1ID"] < 0) & (cellDfWPL["Z"] > np.min(cellDfWPL["Z"]))
        ]
        DFList = [cellDfWPL for i in range(len(lastCellDf))]

        iterableArgs = zip(DFList, lastCellDf["uID"])

        # with mp.Pool(4) as p:
        #     listOfDf = p.starmap(backTrack,iterableArgs)
        with mp.Pool(threads) as p:
            listOfDf = list(tqdm(p.starmap(backTrack, iterableArgs), total=len(DFList)))

    elif mode == "getspecific":
        listOfLinIdx = np.unique(
            cellDfWPL[cellDfWPL["Z"] == np.min(cellDfWPL["Z"])]["cellNo"]
        )
        listOfDf = list()
        missed = 0
        i = 0
        firstCellDf = cellDfWPL[cellDfWPL["Z"] == np.min(cellDfWPL["Z"])]
        uIDs = firstCellDf["uID"].tolist()
        for sCell_id in tqdm(uIDs):
            sCellDf = cellDfWPL[cellDfWPL["uID"] == int(sCell_id)]
            if sCellDf is not None:
                listOfDf.append(sCellDf)
                d2ID = int(sCellDf["daughter2ID"])
                d1ID = int(sCellDf["daughter1ID"])
                while d2ID <= 0:
                    sCellDf = cellDfWPL[cellDfWPL["uID"] == d1ID]
                    if sCellDf.empty:
                        break
                    d2ID = int(sCellDf["daughter2ID"])
                    d1ID = int(sCellDf["daughter1ID"])
                    listOfDf[i - missed] = pd.concat([sCellDf, listOfDf[i - missed]])
                if d2ID > 0:
                    uIDs.append(d2ID)
                    uIDs.append(d1ID)
            else:
                missed = missed + 1
            i = i + 1

    return listOfDf


if __name__ == "__main__":
    from .annotateLineageIdx import annotateLineageIdx

    matFilePath = (
        "/Users/itabashi/Research/Analysis/Schnitzcells/2019-01-02/488/data/488_lin.mat"
    )
    segImgsPath = (
        "/Users/itabashi/Research/Analysis/Schnitzcells/2019-01-02/488/segmentation/"
    )
    rawImgsPath = (
        "/Users/itabashi/Research/Experiment/microscope/2019/01/02/ECTC/Pos0/488"
    )
    cellDf = annotateLineageIdx(matFilePath, segImgsPath, rawImgsPath)
    lineageList = getIndependentLineage(cellDf, "area")
    print(lineageList)
