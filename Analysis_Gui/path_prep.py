import os
import glob
import datetime

'''
Sets needed directory paths from root dir; must have certain structure as below

root
- raw imgs
- saveimg(Schnitzcells root directory)
  - (laser base name)
    - segmentation
    - data
      - (laser base name)_lin.mat

'''

def path_prep (Dir):
        prep_paths = {}
        actual_dir = os.path.join(Dir,'saveimg')
        files = glob.glob(os.path.join(actual_dir,'*'))
        max_date = datetime.date(1,1,1)
        for name in files:
            date = os.path.basename(name).split('-')
            if len(date) == 3:
                date = datetime.date(int(date[0]),int(date[1]),int(date[2]))
                if date > max_date:
                    max_date = date
        recent =  str(max_date)
        data_file = os.path.join(actual_dir,recent)
        
        prep_paths['matFilePath'] = os.path.join(data_file,'405/data/405_lin.mat')
        prep_paths['segImgsPath'] = os.path.join(data_file,'405/segmentation/')
        prep_paths['rawImgsPath'] = os.path.join(Dir,'Ratio')
        return prep_paths    

if __name__ == "__main__":
        sampleDir='/Users/nakatani/LAB/2019_M1/results/TmLps/samples/glc_poor/sample_3_1230_E6/Pos0'
        paths = path_prep(sampleDir)
