#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# -*- coding: utf-8 -*-
#
# Last modified: Thu, 29 Nov 2018 15:17:24 +0900
import math
import colorsys


def createUniqueColorList(count, hue=0, saturation=1.0, value=1.0):
    '''
    Create a unique color list

    Parameters
    ----------
    count : Length of output list.
    hue(optional) : Normalized hue in hsv color space.
    saturation(optional) : Normalized saturation in hsv color space.
    value(optional) : Normalized value in hsv color space.

    Returns
    -------
    uColList : List of unique colors
    '''
    gR = (1 + math.sqrt(5)) / 2
    gA = 1 / (gR ** 2)

    uColList = list()
    for i in range(count):
        rgb = colorsys.hsv_to_rgb(h=hue, s=saturation, v=value)
        uColList.append(rgb)
        hue = (hue + gA) - int(hue + gA)

    return uColList


if __name__ == "__main__":
    uColList = createUniqueColorList(10)
    print(uColList)
