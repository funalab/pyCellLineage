#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# -*- coding: utf-8 -*-
#
# Last modified: Tue, 19 Feb 2019 13:04:39 +0900
import os
from scipy import io


def loadMatImgs(matDirPath):
    '''
    Load the segmentated images saved as MAT files.

    Parameters
    ----------
    matDirPath : A directory in which segmentated images are.
                 The names of segmentated images are generally
                 '***seg000.mat'.

    Returns
    -------
    imgs : A list of numpy array.
           Each array corresponds to each segmentated image.
           An order of this list is sorted by frame order.
    '''
    tmpFiles = os.listdir(matDirPath)
    # exclucde hidden files from file list.
    matFiles = [f for f in tmpFiles if not f.startswith('.')]
    # sort MAT files by frame order
    matFiles.sort()

    imgs = list()

    for matFileIdx in range(len(matFiles)):
        matStruct = io.loadmat(os.path.join(matDirPath, matFiles[matFileIdx]))
        if 'Lc' in list(matStruct.keys()):
            imgs.append(matStruct['Lc'])
        elif 'LNsub' in list(matStruct.keys()):
            imgs.append(matStruct['LNsub'])
        else:
            print(('Lc or LNsub do not exist in frame %d.' % matFileIdx))

    return imgs


if __name__ == "__main__":
    # mport skimage
    anaPath = '/Users/itabashi/Research/Analysis'
    matPath = 'Schnitzcells/9999-99-99/488/segmentation'
    imgs = loadMatImgs(os.path.join(anaPath, matPath))
    # skimage.io.imshow(imgs[0])
    print((imgs[0]))
