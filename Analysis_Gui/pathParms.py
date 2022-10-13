# ## Default Params
import os
import pyCellLineage as myPackage
import sys
'''
Hardwired parameters, path to samples
'''


class pathParms():
    '''
    Paths for samples
    poor_sample_1='/Users/nakatani/LAB/2019_M1/results/TmLps/samples/glc_poor/sample_1_1009_E1/Pos0'
    poor_sample_2='/Users/nakatani/LAB/2019_M1/results/TmLps/samples/glc_poor/sample_2_1223_E3/Pos0'
    poor_sample_3='/Users/nakatani/LAB/2019_M1/results/TmLps/samples/glc_poor/sample_3_1230_E6/Pos0'
    rich_sample_1='/Users/nakatani/LAB/2019_M1/results/TmLps/samples/glc_rich/sample_1_1016_2_E1/Pos0'
    rich_sample_2='/Users/nakatani/LAB/2019_M1/results/TmLps/samples/glc_rich/sample_2_1126_E4/Pos0'
    rich_sample_3='/Users/nakatani/LAB/2019_M1/results/TmLps/samples/glc_rich/sample_3_1203_E1/Pos0'
    '''

    dirPath = str()

    samplePath = dict()

    def __init__(self, dirPath=None):
        if dirPath != None:
            self.dirPath = dirPath
        else:
            dataDir = os.path.join(os.path.dirname(myPackage.__file__), 'Data')

            if os.path.exists(dataDir):
                self.dirPath = dataDir
            else:
                print('ERROR: Something went wrong with data root path')
                sys.exit(-1)

        self.samplePath = {
            'poor': {
                'sample1': os.path.join(self.dirPath, 'glc_poor/sample1/Pos0'),
                'sample2': os.path.join(self.dirPath, 'glc_poor/sample2/Pos0'),
                'sample3': os.path.join(self.dirPath, 'glc_poor/sample3/Pos0')
            },
            'rich': {
                'sample1': os.path.join(self.dirPath, 'glc_rich/sample1/Pos0'),
                'sample2': os.path.join(self.dirPath, 'glc_rich/sample2/Pos0'),
                'sample3': os.path.join(self.dirPath, 'glc_rich/sample3/Pos0')
            }
        }

        return

    def getSamplePath(self):
        return self.samplePath
