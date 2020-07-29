# coding: utf-8
import os
from datetime import datetime
"""
Made to automatically print first line for schnitzcells
copy and paste to matlab command line
rootDir for schnitzcells is set to saveimg by default
"""

def initschnitz(present_path,rootDir="saveimg"):
    _405FS = os.path.join(present_path, "405FS")
    _488FS = os.path.join(present_path, "488FS")
    saveimg = os.path.join(present_path, rootDir)
    if os.path.exists(_405FS) or os.path.exists(_488FS):
        if os.path.exists(_405FS):
            imageDir = os.path.abspath(_405FS)
            basename = "405"
        elif os.path.exists(_488FS):
            imageDir = os.path.abspath(_488FS)
            basename = "488"

        if not os.path.exists(saveimg):
            os.mkdir(saveimg)
        rootDir = os.path.abspath(saveimg)
        print("p = initschnitz(\'%s\',..." %(basename))
        print("\'%s\',..."%(datetime.today().strftime('%Y-%m-%d')))
        print("\'e.coli\',...")
        print("\'rootDir\',\'%s\',..."%(rootDir))
        print("\'imageDir\',\'%s\')"%(imageDir))
    else:
        print("Go to Directory prepared for schnitz\n")


if __name__ == "__main__":
    present_path = os.path.abspath(".")
    initschnitz(present_path)
