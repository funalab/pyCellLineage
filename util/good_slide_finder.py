# coding: utf-8
import pandas as pd
import shutil
import os.path as path
import os
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
from functools import partial
from PIL import Image as pImage
import numpy as np
import skimage.io as sk
import skimage.filters as fil
import scipy.ndimage as ndi


'''
Create result.csv that contains all frame numbers of equally spaced apart 
frames that have been approved by given laser image dir
approval is given using the gui and OK/NG buttons
(No button for redo is set yet and each time the gui starts it erases all previous csv data)
given csv should be 
 slide_num,status

result.csv should be 
 slide_num

using result.csv the program copies the slides deemed good into a new directory good_slide_dir
 

'''


class ImageScreen(BoxLayout):
    def __init__(self, image, **kwargs):
        super(ImageScreen, self).__init__(**kwargs)

        self.orientation = 'vertical'
        lbl = Label(text="Is Image Suitable for Schnitz?\n", font='40sp')
        data = sk.imread(image)
        med_fil = ndi.median_filter(data, size=3)
        otsu_value = fil.threshold_otsu(med_fil)
        binary_array = ((otsu_value < med_fil) * 255).astype(np.uint8)  # image with laser quench to binary
        (pImage.fromarray(binary_array)).save("tmp.png")
        img = Image(source="tmp.png", size_hint_y='120dp')
        img.reload()
        os.remove("tmp.png")

        self.add_widget(lbl)
        self.add_widget(img)


class ButtonScreen(BoxLayout):
    button_bool = True
    img_index = int()
    csv_dir = str()

    def __init__(self, index, csv, sm, **kwargs):
        super(ButtonScreen, self).__init__(**kwargs)

        self. orientation = 'horizontal'
        self.img_index = index
        self.csv_dir = csv
        btn1 = Button(text="OK", font='40sp', size_hint=(None, 0.3))
        btn2 = Button(text="NG", font='40sp', size_hint=(None, 0.3))
        btn1.bind(on_press=partial(self.pressed, status=0, screenmanager=sm))
        btn2.bind(on_press=partial(self.pressed, status=1, screenmanager=sm))

        self.add_widget(btn1)
        self.add_widget(btn2)

    def pressed(self, instance, status, screenmanager):
        good_slide_csv = self.csv_dir
        index = self.img_index
        if index == 0:
            if not path.isfile(good_slide_csv):
                print "created good_slide.csv"
            else:
                print "Found good_slide.csv, Renewed it"
            with open(good_slide_csv, mode='w') as f:
                f.write('slide_num,status\n')

        with open(good_slide_csv, mode='a') as f:
            img_result = str(index) + "," + str(status) + "\n"
            f.write(img_result)
        self.button_bool = False
        screen_list = screenmanager.screen_names
        if len(screen_list) != 1 and index != len(screenmanager.screen_names)-1:
            screen_name = 'image' + str(self.img_index)
            screenmanager.current = screen_list[screen_list.index(screen_name) + 1]
        else:
            fin_screen = Screen(name="end_screen")
            lbl = Label(text="Done!\nClose Window to Resume...")
            fin_screen.add_widget(lbl)
            screenmanager.add_widget(fin_screen)
            screenmanager.current = fin_screen.name


class MainScreen(Screen):
    img_dir = str()
    csv = str()
    btn = object()

    def __init__(self, idx, img, csv, sm,  **kwargs):
        super(MainScreen, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 50
        self.name = 'image' + str(idx)

        self.csv_dir = csv
        self.clear_widgets()
        self.img_index = idx
        self.add_widget(ImageScreen(image=img))
        btn = ButtonScreen(index=self.img_index, csv=csv, sm=sm)
        self.btn = btn
        self.add_widget(btn)
        return


class ImageCheckerApp(App):
    csv = str()
    img_dir = list()

    def build(self):
        self.title = "Good Slide Finder"
        present_path = path.abspath(".")
        target_dir = laser_dir_checker(present_path)
        image_files = sorted(os.listdir(target_dir))
        good_slide_csv = path.join(present_path, "good_slide.csv")
        new_imgs = list()
        for image in image_files:
            abs_image_dir = path.join(target_dir, image)
            if path.isfile(abs_image_dir) and "img" in image:
                new_imgs.append(abs_image_dir)
        if len(new_imgs) == 0:
            print "something went wrong can't find image "
            exit()
        self.csv = good_slide_csv
        self.img_dir = new_imgs
        sm = ScreenManager(transition=NoTransition())
        for image in new_imgs:
            sm.add_widget(MainScreen(sm=sm, idx=new_imgs.index(image), img=image, csv=self.csv))
        sm.current = 'image' + str(0)
        return sm


def laser_dir_checker(present_path):
    target_dir = None
    _405_dir = path.join(present_path, "405")
    if path.isdir(_405_dir):
        target_dir = _405_dir
    else:
        _488_dir = path.join(present_path, "488")
        if path.isdir(_488_dir):
            target_dir = _488_dir
        else:
            print "Not image directory"
            exit()
    return target_dir


def good_itr_find(data, min_slide):
    j = 1
    i = min_slide
    max_slide = data['slide_num'].max()
    while i < max_slide and j < max_slide:
        if data.iloc[i]['status'] == 0:
            i = i + j
        else:
            j += 1
            i = min_slide
    return j


def good_slide_finder(good_slide_dir, dt=30, Td=100):
    good_slide = pd.read_csv(good_slide_dir)
    i = 0
    init_len = good_slide['slide_num'].max()
    min_slide = good_slide['slide_num'].min()
    final_slides = list()
    while init_len > i:
        itr = good_itr_find(good_slide, min_slide)
        if (itr * dt) > Td:
            min_slide = min_slide + 1
            i = i + 1
        else:
            x = good_itr_find(good_slide, min_slide)
            slide = min_slide
            while slide < init_len:
                print good_slide.loc[good_slide['slide_num'] == slide]
                final_slides.append(str(good_slide.iloc[slide]['slide_num']))
                slide = slide + x
            break
    final_result = '\n'.join(final_slides)
    with open(path.join(str(path.split(good_slide_dir)[0]), 'result.csv'), 'w') as f:
        f.write('slide_num\n')
        f.write(final_result)
    print "created result.csv"


def csv_dir_finder(present_csv_dir):
    csv_list = list()
    good_slide_csv = os.path.join(present_csv_dir, "good_slide.csv")
    result_slide_csv = os.path.join(present_csv_dir, "result.csv")

    if os.path.isfile(good_slide_csv):
        csv_list.append(good_slide_csv)
    else:
        print "Oops Something went wrong, can't find csv(%s)\nNot too big of a problem though" % good_slide_csv
        csv_list.append("Null")
    if os.path.isfile(result_slide_csv):
        csv_list.append(result_slide_csv)
    else:
        print "Oops Something went wrong, can't find csv(%s)" % result_slide_csv
        exit()
    return csv_list


def makeid_list(csv_file,basename):
    id_list = list()
    df = pd.read_csv(csv_file)
    for i in range(len(df)):
        id_name = "img_%09d_%s_000.tif" %( df['slide_num'][i],basename)
        id_list.append(id_name)
    return id_list


def good_slide_create(present):
    target_dir = laser_dir_checker(present)
    csv_dirs = csv_dir_finder(present)
    basename = os.path.basename(target_dir)
    dest_name = "good_slide_dir_" + basename
    dest_dir = os.path.join(present, dest_name)
    if not os.path.isdir(dest_dir):
        os.mkdir(dest_dir)
    images = sorted(os.listdir(target_dir))
    id_list = makeid_list(csv_dirs[1], basename)
    for image in images:
        for id_name in id_list:
            if id_name in image:
                src = os.path.join(target_dir, image)
                dest = os.path.join(dest_dir, id_name)
                shutil.copy2(src, dest)


if __name__ == "__main__":
    present_dir = os.path.abspath(".")
    ImageCheckerApp().run()
    good_slide_dir = os.path.abspath("./good_slide.csv")
    good_slide_finder(good_slide_dir)
    good_slide_create(present_dir)
