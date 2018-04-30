# -*- coding: utf-8 -*-
"""
Created on Fri Apr 27 08:22:23 2018

@author: yiyuezhuo

把彩色图提前转成黑白的，操纵亮度使其可以分辨开来。
"""

from PIL import Image
import os


def test():
    global im,im2,im3,im4,test_text
    im = Image.open("images/comb1.png")
    #im2 = im.convert("L")
    im2 = convert(im)
    im3 = Image.open("images/VI11.png")
    #im4 = im3.convert("L")
    im4 = convert(im3)
    test_text='暴力膜蛤必备续'
    
test()
    
def convert(im, mat=(0.55, 0.55, 0.00, 0.0)):
    # matplotlib.colors.cnames
    # red #FF0000, green #008000, blue #0000FF, grey #808080
    return im.convert('RGB').convert('L',mat)

def convert2(im):
    import cv2
    import numpy as np
    
    return Image.fromarray(cv2.decolor(np.array(im.convert('RGB')))[0])

def convert_dir(root, verbose=True):
    root_new = root+'_L'
    os.makedirs(root_new,exist_ok=True)
    for fname in os.listdir(root):
        path = os.path.join(root,fname)
        path_new = os.path.join(root_new,fname)
        im = Image.open(path)
        convert(im).save(path_new)
        if verbose:
            print('{} -> {}'.format(path,path_new))
            