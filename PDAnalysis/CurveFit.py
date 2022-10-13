"""
Author: Joel Nakatani
Overview:

Parameters:
"""

import scipy.optimize import curve_fit
import numpy as np


def expFunc(x,a,b,c):
    return a * np.exp(-b * x) + c

def curveFit(data):
    x,y = data
    popt, pcov = curve_fit(func,x,y)
    print(f'A={popt[0]:.2f}, B={popt[1]:.2f}, C={popt[2]:.2f}')
    return x,expFunc(x,*popt),popt


if __name__ == "__main__":
    
