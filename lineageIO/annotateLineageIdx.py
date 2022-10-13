#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# -*- coding: utf-8 -*-
#
# Last modified: Fri, 14 Oct 2022 02:22:56 +0900
import numpy as np
import pandas as pd
import os

from .measurePhenotypes import measurePhenotypes

from ..util.isNotebook import isnotebook

if isnotebook():
    from tqdm.notebook import tqdm
else:
    from tqdm import tqdm


def annotateLineageIdx(**kwargs):
    if len({"matFilePath", "segImgsPath", "rawImgsPath"} & set(kwargs.keys())) > 2:
        originFrame = 0
        if "originFrame" in kwargs.keys():
            originFrame = kwargs["originFrame"]
        return annotateSchnitz(
            kwargs["matFilePath"],
            kwargs["segImgsPath"],
            kwargs["rawImgsPath"],
            originFrame,
        )
    elif "tanauchi" in kwargs.keys():
        cutOff = None
        if "cutOff" in kwargs.keys():
            cutOff = kwargs["cutOff"]
        return annotateTanauchi(kwargs["tanauchi"], cutOff)
    elif "wang" in kwargs.keys():
        cutOff = None
        if "cutOff" in kwargs.keys():
            cutOff = kwargs["cutOff"]
        return annotateWang(kwargs["wang"], cutOff)
    elif "wakamoto" in kwargs.keys():
        cutOff = None
        if "cutOff" in kwargs.keys():
            cutOff = kwargs["cutOff"]

        return annotateHashimoto(kwargs["wakamoto"], cutOff)

    else:
        print("Error")
        sys.exit(-1)


def annotateWang(WangDir, cutOff=None, fileTag=".dat"):
    coord = sorted(
        [
            os.path.join(WangDir, d)
            for d in os.listdir(WangDir)
            if os.path.isdir(os.path.join(WangDir, d)) and "xy" in d
        ]
    )

    linIdx = 0
    ID = []
    motherID = []
    uID = 0
    Z = []
    intensity = []
    area = []
    daughter1ID = []
    daughter2ID = []
    cenX = []
    cenY = []
    linIdx = []

    lineages = []
    if cutOff is not None:
        x, y = cutOff
        for dName in coord:
            xy = int(dName[-2:])
            if xy <= x:
                lins = sorted(
                    [
                        os.path.join(dName, f)
                        for f in os.listdir(dName)
                        if os.path.isfile(os.path.join(dName, f)) and fileTag in f
                    ]
                )
                lineages += lins[:y]
    else:
        for dName in coord:
            lineages += [
                os.path.join(dName, f)
                for f in os.listdir(dName)
                if os.path.isfile(os.path.join(dName, f)) and fileTag in f
            ]

    for lin in tqdm(lineages):
        cellNo = 0
        with open(lin, "r") as data:
            next(data)
            for line in data:
                if cellNo == 0:
                    motheruID = -1
                else:
                    daughter1ID.append(uID)
                    motheruID = uID - 1
                motherID.append(motheruID)

                ID.append(cellNo)
                aa = line.split(" ")

                cenX.append(float(aa[6]))
                cenY.append(float(aa[7]))
                Z.append(int(aa[0]))
                intensity.append(float(aa[5]))
                area.append(float(aa[4]))  # Acutally Length
                if int(aa[1]) == 1:
                    daughter2ID.append(-3)
                else:
                    daughter2ID.append(-1)
                cellNo += 1
                uID += 1
                linIdx.append(lineages.index(lin))
            daughter1ID.append(-1)
    cellDict = {
        "ID": np.array(ID),
        "uID": np.array(range(uID)),
        "motherID": np.array(motherID),
        "daughter1ID": np.array(daughter1ID),
        "daughter2ID": np.array(daughter2ID),
        "cenX": np.array(cenX),
        "cenY": np.array(cenY),
        "Z": np.array(Z),
        "cellNo": np.array(ID),
        "intensity": np.array(intensity),
        "area": np.array(area),
        "linIdx": np.array(linIdx),
    }
    # for key in cellDict.keys():
    #     print(key,cellDict[key])
    CellDfWP = pd.DataFrame(cellDict)

    return CellDfWP


def annotateTanauchi(TanauchiDir, cutOff=None):
    files = os.listdir(TanauchiDir)
    linIdx = 0
    ID = []
    motherID = []
    uID = 0
    Z = []
    intensity = []
    area = []
    daughter1ID = []
    daughter2ID = []
    cenX = []
    cenY = []
    linIdx = []

    lineages = []
    if cutOff is not None:
        for lin in files:
            x, y = cutOff
            coord = lin[2:].split(".")[0].split("_")
            if int(coord[0]) - 1 < x and int(coord[1]) - 1 < y:
                lineages.append(lin)
    else:
        lineages = files

    for lin in tqdm(lineages):
        cellNo = 0
        coord = lin[2:].split(".")[0].split("_")
        with open(os.path.join(TanauchiDir, lin), "r") as data:
            for line in data:
                cenX.append(int(coord[0]))
                cenY.append(int(coord[1]))
                if cellNo == 0:
                    motheruID = -1
                else:
                    daughter1ID.append(uID)
                    motheruID = uID - 1
                motherID.append(motheruID)

                ID.append(cellNo)
                aa = line.split(",")
                Z.append(int(aa[0]) - 1)
                intensity.append(float(aa[4]))
                area.append(float(aa[2]))  # Acutally Length
                if int(aa[1]) == 1:
                    daughter2ID.append(-3)
                else:
                    daughter2ID.append(-1)
                cellNo += 1
                uID += 1
                linIdx.append(lineages.index(lin))
            daughter1ID.append(-1)
    cellDict = {
        "ID": np.array(ID),
        "uID": np.array(range(uID)),
        "motherID": np.array(motherID),
        "daughter1ID": np.array(daughter1ID),
        "daughter2ID": np.array(daughter2ID),
        "cenX": np.array(cenX),
        "cenY": np.array(cenY),
        "Z": np.array(Z),
        "cellNo": np.array(ID),
        "intensity": np.array(intensity),
        "area": np.array(area),
        "linIdx": np.array(linIdx),
    }
    # for key in cellDict.keys():
    #     print(key,cellDict[key])
    CellDfWP = pd.DataFrame(cellDict)

    return CellDfWP


def annotateHashimoto(HashimotoDir, cutOff=None):
    linIdx = 0
    ID = []
    motherID = []
    uID = 0
    Z = []
    intensity = []
    area = []
    daughter1ID = []
    daughter2ID = []
    cenX = []
    cenY = []

    lineages = []

    columnName = [
        "ID",
        "uID",
        "motherID",
        "daughter1ID",
        "daughter2ID",
        "cenX",
        "cenY",
        "Z",
        "cellNo",
        "intensity",
        "area",
        "linIdx",
    ]
    CellDfWP = pd.DataFrame(columns=columnName)
    data = pd.read_table(HashimotoDir, index_col=0)
    lastCell = data[data["LastIndex"] == 1].sort_index()
    if cutOff is not None:
        lastCell = lastCell.iloc[: int(cutOff)]
    for lCell in tqdm(lastCell.iterrows()):
        progenyId, lCell = lCell
        daughter1ID = -1

        motherId = int(lCell["PreviousCell"])
        while motherId >= 0:
            info = [
                progenyId,
                motherId,
                daughter1ID,
                -1,
                float(lCell["XM"]),
                float(lCell["YM"]),
                lCell["Slice"] - 1,
                float(lCell["Mean"]) - float(lCell["Background"]),
                float(lCell["Area"]),
                linIdx,
            ]  #  Add row with this info
            columns = columnName[1:8] + columnName[-3:]  # skip over ID and cellNo
            df = dict(zip(columns, info))

            if motherId in list(CellDfWP["uID"]) and motherId != 0:
                mask = CellDfWP["uID"] == motherId
                CellDfWP.loc[mask, "daughter2ID"] = progenyId

                d1 = CellDfWP.loc[mask, "daughter1ID"]
                d2 = CellDfWP.loc[mask, "daughter2ID"]
                if int(d1) > int(d2):
                    tmp = int(d1)
                    d1 = int(d2)
                    d2 = tmp

                maskLin = CellDfWP["linIdx"] == linIdx
                linIdx -= 1
                CellDfWP.loc[maskLin, "linIdx"] = int(CellDfWP.loc[mask, "linIdx"])
                CellDfWP = CellDfWP.append(df, ignore_index=True)
                break
            #                CellDfWP[CellDfWP['uID'] == motherId]['daughter2ID'] = progenyId
            daughter1ID = progenyId
            progenyId = motherId

            if motherId == 0:
                motherId = -1
                df["motherID"] = motherId
            else:
                lCell = data.iloc[motherId - 1]
                motherId = int(lCell["PreviousCell"])

            CellDfWP = CellDfWP.append(df, ignore_index=True)
        linIdx += 1

    CellDfWP = CellDfWP.sort_values(by="Z", ascending=True)
    CellDfWP["ID"] = list(range(len(CellDfWP)))
    CellDfWP["cellNo"] = list(range(len(CellDfWP)))
    # CellDfWP['uID'] = CellDfWP['uID'].astype(int)
    # CellDfWP['motherID'] = CellDfWP['motherID'].astype(int)
    # CellDfWP['daughter1ID'] = CellDfWP['daughter1ID'].astype(int)
    # CellDfWP['daughter2ID'] = CellDfWP['daughter2ID'].astype(int)
    # CellDfWP['Z'] = CellDfWP['Z'].astype(int)
    # CellDfWP['linIdx'] = CellDfWP['linIdx'].astype(int)
    return CellDfWP


def annotateSchnitz(matFilePath, segImgsPath, rawImgsPath, originFrame=0):
    """
    Annotate lineage indices accorting to the result of cell tracking.

    Parameters
    ----------
    matFilePath : string
                  A path to MAT files which were created by Schnitzcells
    segImgsPath : string
                  A path to directory which include segmentated images which
                  were created by Schnitzcells
    rawImgsPath : string
                  A path to direcotry which include raw images
                  which were required for Schnitzcells

    Returns
    -------
    cellDfWPL : pandas.core.frame.DataFrame
                A pandas dataframe which includes tracking result and
                phenotypes of each cell, lineage indices.
                Its name is abbreviate for cell DataFrame
                With Phenotypes, Lineage indices.
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
                - linIdx
    """
    cellDfWP = measurePhenotypes(matFilePath, segImgsPath, rawImgsPath, originFrame)

    numOfLin = 0
    for uID in cellDfWP["uID"]:
        daughter1ID = cellDfWP["daughter1ID"][uID]
        daughter2ID = cellDfWP["daughter2ID"][uID]
        if daughter1ID < 0 and daughter2ID < 0:
            numOfLin += 1

    linIdx = 0
    linList = np.zeros(len(cellDfWP["uID"]))

    for uID in cellDfWP["uID"]:
        motherID = cellDfWP["motherID"][uID]

        if motherID == -1:
            linList[uID] = linIdx
            linIdx += 1
        else:
            sister1ID = cellDfWP["daughter1ID"][motherID]
            sister2ID = cellDfWP["daughter2ID"][motherID]
            if sister1ID > 0 and sister2ID > 0:  # 親が分裂していたら
                if sister1ID == uID:
                    linList[uID] = linList[motherID]
                else:
                    linList[uID] = linIdx
                    linIdx += 1
            else:  # 親が分裂していなかったら
                linList[uID] = linList[motherID]

    linIdx = 0
    for uID in cellDfWP["uID"]:
        motherID = cellDfWP["motherID"][uID]

        if motherID == -1:
            linList[uID] = linIdx
            linIdx += 1
        else:
            sister1ID = cellDfWP["daughter1ID"][motherID]
            sister2ID = cellDfWP["daughter2ID"][motherID]
            if sister1ID > 0 and sister2ID > 0:  # 親が分裂していたら
                if sister1ID == uID:
                    linList[uID] = linList[motherID]
                else:
                    linList[uID] = linIdx
                    linIdx += 1
            else:  # 親が分裂していなかったら
                linList[uID] = linList[motherID]

    linList = linList.astype(np.int64)
    cellDfWP["linIdx"] = linList

    return cellDfWP


if __name__ == "__main__":
    matFilePath = (
        "/Users/itabashi/Research/Analysis/Schnitzcells/"
        "9999-99-99/488/data/488_lin.mat"
    )
    segImgsPath = (
        "/Users/itabashi/Research/Analysis/Schnitzcells/" "9999-99-99/488/segmentation/"
    )
    rawImgsPath = (
        "/Users/itabashi/Research/Experiment/microscope/"
        "2018/08/28/ECTC_8/Pos0/forAnalysis/488FS/"
    )
    cellDfWPL = annotateLineageIdx(matFilePath, segImgsPath, rawImgsPath)
    print(cellDfWPL)
