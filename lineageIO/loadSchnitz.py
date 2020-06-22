#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# -*- coding: utf-8 -*-
#
# Last modified: Sat, 02 Feb 2019 13:55:21 +0900
import numpy as np
import pandas as pd
from scipy import io

from flattenList import flattenList


def loadSchnitz(matFilePath):
    '''
    Load the result of tracking done by Schnitzcells and
    convert it into human readable dataframe.

    Parameters
    ----------
    matFilePath : A path of MAT file which will be created by Schnitzcells.
                  Its name may be '*_lin.mat'.

    Returns
    -------
    cellDf : A pandas dataframe which includes tracking result.
             Its name is abbreviate for cell DataFrame.
             Column indices are like below.
             - ID
             - uID
             - motherID
             - daughter1ID
             - daughter2ID
             - cenX
             - cenY
             - Z
             - cellNo
    '''
    # load MAT file and flatten nested list
    matFile = io.loadmat(matFilePath)
    tmpList = list()
    for matInfo in matFile:
        if '__' not in matInfo and 'readme' not in matInfo:
            matFile[matInfo] = flattenList(matFile[matInfo])

            lenOfRow = len(matFile[matInfo])
            for rowIdx in range(lenOfRow):
                lenOfField = len(matFile[matInfo][rowIdx])
                for fieldIdx in range(lenOfField):
                    flattened = flattenList(matFile[matInfo][rowIdx][fieldIdx])
                    matFile[matInfo][rowIdx][fieldIdx] = np.array(flattened)

                tmpList.append(matFile[matInfo][rowIdx])

    # create dataframe from the list
    tmpList = np.array(tmpList)
    tmpDf = pd.DataFrame(tmpList)

    # set the start of each index as zero
    tmpDf['P'] = tmpDf['P'] - 1
    tmpDf['frames'] = tmpDf['frames'] - 1
    tmpDf['cellno'] = tmpDf['cellno'] - 1
    tmpDf['D'] = tmpDf['D'] - 1
    tmpDf['E'] = tmpDf['E'] - 1

    # use only approved frames
    #tmpDf = tmpDf[tmpDf['approved']==1]
    # fix N values with actual length of frames
    for i in range(len(tmpDf['N'])):
        tmpDf['N'][i] = np.array([len(tmpDf['frames'][i])])

    uCellNum = 0
    uID = list()
    ID = list()
    motherID = list()
    daughter1ID = list()
    daughter2ID = list()
    cenX = list()
    cenY = list()
    Z = list()
    cellNo = list()

    for i in range(len(tmpDf)):
        if len(tmpDf['N'][i]) != 0:
            for j in range(tmpDf['N'][i]):
                ID.append(i)
                uID.append(uCellNum)
                uCellNum += 1

    cellDf = pd.DataFrame({'ID': np.array(ID), 'uID': np.array(uID)})

    # IDを順に上から見ていく
    # lineageIdx = no. of Schnitz
    for lineageIdx in range(len(tmpDf)):
        boolList = cellDf['ID'] == lineageIdx
        uIDList = cellDf['uID'][boolList].values
        # あるIDにふくまれるframesをみる
        if len(tmpDf['frames'][lineageIdx]) != 0:
            for timeInsideLin in range(len(tmpDf['frames'][lineageIdx])):
                # annotate motherID
                if timeInsideLin == 0:  # 見ているUIDがIDの中で一番小さいものだった場合
                    boolList = cellDf['ID'] == tmpDf['P'][lineageIdx][0]
                    if boolList.any():
                        listOfSomeUID = cellDf['uID'][boolList].values
                        motherID.append(listOfSomeUID[-1])
                    else:
                        motherID.append(-1)
                else:
                    motherID.append(uIDList[timeInsideLin] - 1)

                # annotate daughterIDs
                # 見ているUIDがIDの中で最も大きいものだった場合
                if timeInsideLin == tmpDf['N'][lineageIdx] - 1:
                    boolListD1 = cellDf['ID'] == tmpDf['D'][lineageIdx][0]
                    boolListD2 = cellDf['ID'] == tmpDf['E'][lineageIdx][0]

                    if boolListD1.any():
                        listOfSomeUID = cellDf['uID'][boolListD1].values
                        daughter1ID.append(listOfSomeUID[0])
                    else:
                        daughter1ID.append(-1)  # 最後のタイムポイント

                    if boolListD2.any():
                        listOfSomeUID = cellDf['uID'][boolListD2].values
                        daughter2ID.append(listOfSomeUID[0])
                    else:
                        daughter2ID.append(-1)  # 最後のタイムポイント
                else:
                    daughter1ID.append(uIDList[timeInsideLin] + 1)
                    daughter2ID.append(-2)

                # annotate coordinates
                cenX.append(tmpDf['cenx'][lineageIdx][timeInsideLin])
                cenY.append(tmpDf['ceny'][lineageIdx][timeInsideLin])
                Z.append(tmpDf['frames'][lineageIdx][timeInsideLin])

                # annotate cell no. within a frame
                cellNo.append(tmpDf['cellno'][lineageIdx][timeInsideLin])

    cellDf['motherID'] = motherID
    cellDf['daughter1ID'] = daughter1ID
    cellDf['daughter2ID'] = daughter2ID
    cellDf['cenX'] = cenX
    cellDf['cenY'] = cenY
    cellDf['Z'] = Z
    cellDf['cellNo'] = cellNo
    #cellDf=cellDf.sort_values('Z')
    #fixed bug in schnitzcells where cellNo is weird when there is a division on the last frame
    last_cells = cellDf.loc[cellDf['Z']==max(cellDf['Z'])].loc[cellDf['daughter1ID']!=-1]['uID']
    for uID in last_cells:
            cellDf.loc[uID,'daughter1ID'] = -1
            cellDf.loc[uID,'daughter2ID'] = -1
    return cellDf


if __name__ == "__main__":
    import os
    anaPath = '/Users/itabashi/Research/Analysis'
    matPath = 'Schnitzcells/9999-99-99/488/data/488_lin.mat'
    cellDf = loadSchnitz(os.path.join(anaPath, matPath))
    print(cellDf)
