#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# -*- coding: utf-8 -*-
#
# Last modified: Wed, 12 Dec 2018 00:35:27 +0900
import numpy as np
import os
from skimage import io


def loadRawImgs(rawImgsPath):
    '''
    Load raw image sequence as list

    Parameters
    ----------
    rawImgsPath : A directory in which segmentated images are.
                 The names of segmentated images are generally
                 '***seg000.mat'.

    Return value
    ------------
    imgs : A list of segmentated images which Schnitzcells outputs.
           An order of this list is sorted by frame order
    '''
    tmpFiles = os.listdir(rawImgsPath)
    # exclude hidden files from file list.
    rawImgFiles = [f for f in tmpFiles if not f.startswith('.')]
    # sort image files by frame order
    rawImgFiles.sort()

    imgs = list()

    for f in rawImgFiles:
        img = io.imread(os.path.join(rawImgsPath, f))
        img = np.where(img == np.infty, 0, img)
        imgs.append(img)

    return imgs


if __name__ == "__main__":
    micPath = '/Users/itabashi/Research/Experiment/microscope/'
    rawPath = '2018/08/28/ECTC_8/Pos0/forAnalysis/488'
    imgs = loadRawImgs(os.path.join(micPath, rawPath))
    print(imgs[0])
