# coding: utf-8
import os
import sys
from datetime import datetime
"""
Made to automatically print first line for schnitzcells
copy and paste to matlab command line
rootDir for schnitzcells is set to saveimg by default
"""

def initschnitz(present_path,rootDir="saveimg",FS="..."):
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
        print("p = initschnitz(\'%s\',%s" %(basename,FS))
        print("\'%s\',%s" %(datetime.today().strftime('%Y-%m-%d'),FS))
        print("\'e.coli\',%s" %(FS))
        print("\'rootDir\',\'%s\',%s" %(rootDir,FS))
        print("\'imageDir\',\'%s\')"%(imageDir))
    else:
        print("Go to Directory prepared for schnitz\n")


if __name__ == "__main__":
    args = sys.argv
    if len(args)!=1:
        for i in range(len(args)):
            arg = args[i]
            if arg[0] == "-":
                if arg[1] == "F":
                    if i+1 > len(args)-1:
                        foption = ""
                    else:
                        foption = args[i+1]
    else:
        foption = "..."
    present_path = os.path.abspath(".")
    if foption != None:
        initschnitz(present_path,FS=foption)
    else:
        initschnitz(present_path)
