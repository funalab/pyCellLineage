import pandas as pd
import sys
import os


def atpCalib(intensity, emax=None, d=None, EC50=None, atp_path=None):
    if emax is None or d is None or EC50 is None:
        if atp_path is None or not os.path.isfile(atp_path):
            print("Must Provide correct Path to atp_calib.csv")
            sys.exit(-1)
        else:
            print("reading from " + atp_path + "\n Extracting new values...")
            atp_df = pd.read_csv(atp_path)
            emax = float(atp_df[atp_df['parameter'] == 'Emax']['value'])
            d = float(atp_df[atp_df['parameter'] == 'd']['value'])
            EC50 = float(atp_df[atp_df['parameter'] == 'EC50']['value'])
    if float(intensity) < d:
        return 0
#    elif float(intensity) > emax:
#        return (((emax-d)/emax*((EC50)**2)) / (1-((emax-d)/emax)))**0.5
    else:
        return (((float(intensity)-d)/emax*((EC50)**2))/(1-((float(intensity)-d)/emax)))**0.5
