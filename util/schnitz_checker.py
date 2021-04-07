from datetime import datetime,timedelta
import os

def schnitz_checker(target):
    for days_ago in range(100):
        schnitz_dir = os.path.join(target,"saveimg/%s" % (datetime.today()-timedelta(days_ago)).strftime('%Y-%m-%d'))
        if os.path.isdir(schnitz_dir):
            break
    print("Target:" + schnitz_dir)
    matFilePath = os.path.join(target,'saveimg/%s/405/data/405_lin.mat' %(datetime.today()-timedelta(days_ago)).strftime('%Y-%m-%d'))
    segImgsPath = os.path.join(target, 'saveimg/%s/405/segmentation/' % (datetime.today()-timedelta(days_ago)).strftime('%Y-%m-%d'))
    rawImgsPath = os.path.join(target, 'Ratio')
    print("MatFile:" + matFilePath)
    print("SegImgs:" + segImgsPath)
    print("rawImgs:" + rawImgsPath)
    return matFilePath, segImgsPath, rawImgsPath

if __name__ == "__main__":
    target = input("What is the absolute target path? (Pos0)")
    schnitz_checker(target)
