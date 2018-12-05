#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# -*- coding: utf-8 -*-
#
# Last modified: Wed, 05 Dec 2018 14:00:30 +0900


def main():
    import os
    import sys
    import glob
    import shutil
    import re

    argn = len(sys.argv) - 1

    if argn != 1:
        print('Specify the target directory.')
        sys.exit()

    sourceDir = os.path.abspath(sys.argv[1])
    fileList = glob.glob(sourceDir + '/*.tif')
    baseName = os.path.basename(sourceDir)

    if re.search('405', baseName):
        base = '405'
    elif re.search('488', baseName):
        base = '488'
    elif re.search('BF', baseName):
        base = 'BF'
    elif re.search('Phase', baseName):
        base = 'Phase'
    else:
        print('the name of directory does not contain an information about laser strength.')
        sys.exit()

    parentDir = os.path.dirname(sourceDir)
    targetDir = os.path.join(parentDir, baseName + 'FS')

    if not os.path.exists(targetDir):
        os.mkdir(targetDir)
        for i in range(0, len(fileList)):
            sourceNameRE = 'img_%09d_' % i + base
            # sourceNameRE = '%05d' % i
            for name in fileList:
                if re.search(sourceNameRE, name):
                    sourceName = name
            sourceFile = os.path.join(sourceDir, sourceName)
            if baseName == '405' or baseName == '488':
                targetName = base + '-g-' + '%03d' % i + '.tif'
            else:
                targetName = base + '-p-' + '%03d' % i + '.tif'
            targetFile = os.path.join(targetDir, targetName)
            shutil.copy2(sourceFile, targetFile)


if __name__ == "__main__":
    main()
