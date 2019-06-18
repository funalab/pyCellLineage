# coding: utf-8
import os
import shutil

def main():
    if os.path.exists("405"):
        if not os.path.exists("macro"):
            os.mkdir("macro")
            if os.path.isdir("405"):    
                file_len = len(os.listdir("405"))
        else:
            print "Wrong Directory?\n"
            exit()
        print "File is from 1~"+str(file_len)+"\n"
        file_num = int(raw_input("Which file would you like to make a ratio for?\n"))
        file_num_img = file_num - 1
        file_num_sntz = file_num
        file_name_405 = '405/img_%09d_405_000.tif' %(file_num_img)
        file_name_488 = '488/img_%09d_488_000.tif' %(file_num_img)
        file_name_sntz = "seg_img/"+str(file_num_sntz) + ".tif"
        if os.path.exists(file_name_405):
            shutil.copy2(file_name_405,"macro/405.tif")#405
        if os.path.exists(file_name_488):
            shutil.copy2(file_name_488,"macro/488.tif")#488
        if os.path.exists(file_name_sntz):
            shutil.copy2(file_name_sntz,"macro/seg.tif")#seg  
        if os.path.exists("window.roi"):
            shutil.copy2("window.roi","macro/window.roi")#window.roi
        else:
            print "window.roi doesn't exist something went wrong!\n"                              
    else:
        print "Go to proper Directory!\n"
            
if __name__ == "__main__":
    main()
