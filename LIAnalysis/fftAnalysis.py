#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# -*- coding: utf-8 -*-
#
# Last modified: Mon, 28 Jan 2019 14:31:47 +0900
import numpy
import os
import pandas as pd
from pyLineage.lineageIO.getIndependentLineage import getIndependentLineage


def write_ATPChange(CellDF,save_dir):
    counter = int(0)
    if not os.path.isdir(save_dir):
        os.mkdir(save_dir)
    for lineage in getIndependentLineage(CellDF):
        lin_change = list()
        time_change = list()
        
        for cell_id in lineage['uID']:
            cell = CellDF[CellDF['uID'] == cell_id]
            lin_change.append(float(cell['ATP']))
            time_change.append(int(cell['Z']))
        dict = {'time':time_change,'atp':lin_change}
        df = pd.DataFrame(dict)
        df.to_csv(os.path.join(save_dir,str(counter)+".csv"))
        counter = counter + 1
            
def fftAnalysis(cellDfWPL):
    '''
    Analysis all lineages with Fast Fourier Transform.

    Parameters
    ----------
    cellDfWPL

    Returns
    -------
    '''



if __name__ == "__main__":
    main()
