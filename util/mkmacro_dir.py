# coding: utf-8
import os
import shutil


def main():
    file_len = None
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
        file_name_405 = os.path.abspath(os.path.join("405", 'img_%09d_405_000.tif' % file_num_img))
        file_name_488 = os.path.abspath(os.path.join("488", 'img_%09d_488_000.tif' % file_num_img))
        file_name_sntz = os.path.abspath(os.path.join("seg_img", str(file_num_sntz) + ".tif"))
        if os.path.exists(file_name_405):
            des = os.path.join(os.path.abspath("macro"), "405.tif")
            if not os.path.isdir(os.path.abspath("macro")):
                shutil.copy2(file_name_405, des)  # 405
            else:
                print "Couldn't move 405!\n"
        if os.path.exists(file_name_488):
            des = os.path.join(os.path.abspath("macro"), "488.tif")
            if not os.path.isdir(os.path.abspath("macro")):
                shutil.copy2(file_name_488, des)  # 488
            else:
                print "Couldn't move 488!\n"
        if os.path.exists(file_name_sntz):
            des = os.path.join(os.path.abspath("macro"), "seg.tif")
            if not os.path.isdir(os.path.abspath("macro")):
                shutil.copy2(file_name_sntz, des)  # seg
            else:
                print "Couldn't move segment file!\n"
        if os.path.exists(os.path.abspath("window.roi")):
            des = os.path.join(os.path.abspath("macro"), "window.roi")
            if not os.path.isdir(os.path.abspath("macro")):
                shutil.copy2("window.roi", des)  # window.roi
            else:
                print "Couldn't move roi!\n"
        else:
            print "window.roi doesn't exist something went wrong!\n"                              
    else:
        print "Go to proper Directory!\n"


if __name__ == "__main__":
    main()
