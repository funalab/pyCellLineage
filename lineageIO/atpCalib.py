import pandas as pd
import sys
import os
import numpy as np
import pyCellLineage.lineageIO as myPackage


def atpCalib(intensity, emax=None, d=None, EC50=None, atp_path=None):
    if emax is None or d is None or EC50 is None:
        if atp_path is None or not os.path.isfile(atp_path):
            atp_path = os.path.join(os.path.dirname(myPackage.__file__),
                                    "atp_calib.csv")
        else:
            print("reading from " + atp_path + "\n Extracting new values...")
        atp_df = pd.read_csv(atp_path)
        emax = float(atp_df[atp_df['parameter'] == 'Emax']['value'])
        d = float(atp_df[atp_df['parameter'] == 'd']['value'])
        EC50 = float(atp_df[atp_df['parameter'] == 'EC50']['value'])

    if float(intensity) < d or float(intensity) == float('inf'):
        return 0
    elif float(intensity) > emax:
        #print "[Warning]: Exceeds max intensity capable of measuring(Ratio:"+str(intensity)+")\n"

        return np.nan
    else:
        return (((float(intensity) - d) / emax * ((EC50)**2)) /
                (1 - ((float(intensity) - d) / emax)))**0.5
