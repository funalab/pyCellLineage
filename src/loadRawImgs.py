#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# -*- coding: utf-8 -*-
#
# Last modified: Wed, 28 Nov 2018 17:35:01 +0900
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
        imgs.append(io.imread(os.path.join(rawImgsPath, f)))

    return imgs


if __name__ == "__main__":
    micPath = '/Users/itabashi/Research/Experiment/microscope/'
    rawPath = '2018/08/28/ECTC_8/Pos0/forAnalysis/488'
    imgs = loadRawImgs(os.path.join(micPath, rawPath))
    print(imgs[0])
