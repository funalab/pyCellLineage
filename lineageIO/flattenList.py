#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# -*- coding: utf-8 -*-
#
# Last modified: Wed, 28 Nov 2018 13:25:08 +0900


def flattenList(nestedList):
    '''
    Flatten nested lists.

    Parameters
    ----------
    nestedlist : nested list

    Returns
    -------
    A list object which was flattened.
    '''
    if len(nestedList) == 1:
        return nestedList[0]
    else:
        return [e for innerList in nestedList for e in innerList]


if __name__ == "__main__":
    flattenList([[1, 2, 3], [4, 5, 6], [[7, 8, 9]]])
