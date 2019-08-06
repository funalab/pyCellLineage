from annotateLineageIdx import annotateLineageIdx
from loadMatImgs import loadMatImgs
import os


def lineage_editor(matFilePath, segImgsPath, rawImgsPath, originFrame=0, mode=1):
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
            prv_mode = mode
    if mode == 2:  # use images to find correct centroid
        segImgsPath = os.path.join(segImgsPath, os.listdir(segImgsPath))
        for time_frame in bad_place['Z']:
            target = segImgsPath[time_frame - originFrame]
            loadMatImgs()




    return DF


if __name__ == "__main__":
    filepath = ()
    lineage_editor(file_path[0], filepath[1], filepath[2])
