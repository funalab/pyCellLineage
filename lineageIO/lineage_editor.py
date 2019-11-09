from annotateLineageIdx import annotateLineageIdx
from loadMatImgs import loadMatImgs
import os
from loadMatImgs import loadMatImgs
from loadRawImgs import loadRawImgs
from extractIntensity import extractIntensity
from PIL import Image
from skimage import measure
from skimage import morphology
import operator
import collections
import numpy as np
import sys


def lineage_editor(matFilePath, segImgsPath, rawImgsPath, originFrame=0, mode=2, DF=None):
    if DF is None:
        DF = annotateLineageIdx(matFilePath, segImgsPath, rawImgsPath, originFrame)
    bad_place = DF[DF['cenX'] == 0]
    prv_mode = None
    if mode == 1:  # find cells at weird positions and bring them to the correct place (linear)
        for value in bad_place['uID']:
            bad_cell = bad_place[bad_place['uID'] == value]
            m_ID = bad_cell['motherID'].values[0]
            d_ID = bad_cell['daughter1ID'].values[0]

            d_cell = DF[DF['uID'] == d_ID]
            if m_ID == -1:
                m_cell = d_cell
            else:
                m_cell = DF[DF['uID'] == m_ID]
                if d_ID == -2:
                    d_cell = m_cell
            m_ID_cen = (m_cell['cenX'].values[0], m_cell['cenY'].values[0])
            d_ID_cen = (d_cell['cenX'].values[0], d_cell['cenY'].values[0])
            DF.loc[value, 'cenX'] = (d_ID_cen[0] + m_ID_cen[0]) / 2
            DF.loc[value, 'cenY'] = (d_ID_cen[1] + m_ID_cen[1]) / 2

    if mode == 2:  # use images to find correct centroid
        for value in bad_place['uID']:
            bad_cell = bad_place[bad_place['uID'] == value]
            time_frame = bad_cell['Z'].values[0]
            cellNo = bad_cell['cellNo'].values[0]
            data = loadMatImgs(segImgsPath)
            segImg = data[time_frame + originFrame]
            data = loadRawImgs(rawImgsPath)
            rawImg = data[time_frame + originFrame]
            total = {}
            added_total = 0
            for i in range(max(DF['Z'])):
                cell_count = len(DF[DF['Z'] == i])
                added_total = cell_count + added_total
                total[i] = added_total
            meanIntDict = extractIntensity(segImg, rawImg)
            Intensity_ranking = sorted(meanIntDict.items(), key=lambda x: x[1])
            Intensity_ranking = collections.OrderedDict(Intensity_ranking)
            cellIdx = None
            Intensity = Intensity_ranking[cellNo]

            binaryCellMask = segImg == cellNo
            contour = measure.find_contours(binaryCellMask, 0)
            EM = measure.EllipseModel()
            EM.estimate(contour[0])
            xc, yc, a, b, theta = EM.params
            if a < b:
                medianCellWidth = a
            else:
                medianCellWidth = b

            erodeMask = segImg == cellNo
            erodeIter = int(medianCellWidth / 4)
            for i in range(erodeIter):
                erodeMask = morphology.binary_erosion(erodeMask,
                                                      selem=np.ones((3, 3)))
            area = np.sum(erodeMask)
            intensity = np.sum(rawImg * erodeMask)
            if Intensity == intensity/area:
                DF.loc[value, 'cenX'] = xc
                DF.loc[value, 'cenY'] = yc
            else:
                print "Can't find one"
                sys.exit()
    if mode==3:
        for value in DF['uID']:
            cell = DF[DF['uID'] == value]
            m_ID = cell['motherID'].values[0]
            d_ID = cell['daughter1ID'].values[0]

            d_cell = DF[DF['uID'] == d_ID]
            if m_ID == -1:
                m_cell = d_cell
            else:
                m_cell = DF[DF['uID'] == m_ID]
                if d_ID == -2:
                    d_cell = m_cell
            m_ID_cen = (m_cell['cenX'].values[0], m_cell['cenY'].values[0])
            d_ID_cen = (d_cell['cenX'].values[0], d_cell['cenY'].values[0])
            if (DF.loc[value, 'cenX'] - (d_ID_cen[0] + m_ID_cen[0])/2) > 400 or DF.loc[value,'cenX'] == np.nan:
                bad_cell = DF[DF['uID'] == value]
                time_frame = bad_cell['Z'].values[0]
                cellNo = bad_cell['cellNo'].values[0]
                data = loadMatImgs(segImgsPath)
                segImg = data[time_frame + originFrame]
                data = loadRawImgs(rawImgsPath)
                rawImg = data[time_frame + originFrame]
                total = {}
                added_total = 0
                for i in range(max(DF['Z'])):
                    cell_count = len(DF[DF['Z'] == i])
                    added_total = cell_count + added_total
                    total[i] = added_total
                meanIntDict = extractIntensity(segImg, rawImg)
                Intensity_ranking = sorted(meanIntDict.items(), key=lambda x: x[1])
                Intensity_ranking = collections.OrderedDict(Intensity_ranking)
                cellIdx = None
                Intensity = Intensity_ranking[cellNo]
                
                binaryCellMask = segImg == cellNo
                contour = measure.find_contours(binaryCellMask, 0)
                EM = measure.EllipseModel()
                EM.estimate(contour[0])
                xc, yc, a, b, theta = EM.params
                if a < b:
                    medianCellWidth = a
                else:
                    medianCellWidth = b
                    
                erodeMask = segImg == cellNo
                erodeIter = int(medianCellWidth / 4)
                for i in range(erodeIter):
                    erodeMask = morphology.binary_erosion(erodeMask,
                                                          selem=np.ones((3, 3)))
                area = np.sum(erodeMask)
                intensity = np.sum(rawImg * erodeMask)
                if Intensity == intensity/area:
                    DF.loc[value, 'cenX'] = xc
                    DF.loc[value, 'cenY'] = yc
                else:
                    print "Can't find one"
                    sys.exit()
            

    CellDFWPL = DF
    return CellDFWPL


if __name__ == "__main__":
    filepath = ()
    lineage_editor(file_path[0], filepath[1], filepath[2])
