#!/usr/bin/env python
# coding: utf-8

"""
Created 2021/2022

@author: Peter Hebden, phebden@gmail.com
"""

import cv2
import imutils
import os
from shutil import copyfile

# For each original image, generate rotated versions to build
# an augmented data set. Save each image and its rotated versions to a 
# destination folder that will contain images from one or more days of 
# images, e.g. taken on the August 25th and 26th.


data_originals = ["images-25-orange-white/", "images-26-orange-white/"]

# change this to your source image data path
src_folder=data_originals[1]   # original images, source folder
                               # orginal 1600x1600 pixel images
dest_folder="images-25-26-orange-white/train/" # destination folder

angles     =[ 90,  180,  -90]
angle_label=['90','180','270']

for src_folder in data_originals:

    files = os.listdir(src_folder)
    
    for filename in files:
        #print(filename)
        # just want to load the original images
        if not filename.endswith(".jpg") or filename.find("-rot-") >= 0:
            continue
    
        src_path = src_folder + filename
        src = cv2.imread(src_path) 
        
        # orginal image
        dest_path = f'{dest_folder}{filename}'
        print(dest_path)
        cv2.imwrite(dest_path, src)
        
        new_filename=filename.replace('.jpg', '.xml')
        src_path = src_folder + new_filename
        dest_path = f'{dest_folder}{new_filename}'
        print(dest_path)
        copyfile(src_path, dest_path)
    
        #rotation angle in degrees
        #rotated = imutils.rotate(src,angle)
    
        for ii in range(len(angles)):
            rotated_image = imutils.rotate(src,angles[ii])
            new_ext = '-rot-' + angle_label[ii] + '.jpg'
            new_filename=filename.replace('.jpg', new_ext)
            dest_path = f'{dest_folder}{new_filename}'
            print(dest_path)
            cv2.imwrite(dest_path, rotated_image)
    

    
  

      
    
    
 

