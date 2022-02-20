#!/usr/bin/env python
# coding: utf-8

# In[58]:


import cv2
#import matplotlib.pyplot as plt
import os
from scipy import ndimage
import matplotlib.pyplot as plt

data_set = 'images-rot/'

class_names = ['car']


files = os.listdir(data_set)
# path_to_labels =  f'{folder}/labels.txt'
# f=open(path_to_labels)
# the_labels = f.readlines()
# the_labels = "".join(the_labels)
# f.close()

for filename in files:
    #print(filename)
    if not filename.endswith("jpg"):
        continue
    # path 
    path = f'{data_set}{filename}'
    print(path)

    src = cv2.imread(path) 
    
    #rotation angle in degree
    rotated = ndimage.rotate(src, -90)
    new_filename=filename.replace('.jpg', '-rot-90.jpg')
    new_path = f'{data_set}{new_filename}'
    print(new_path)
    cv2.imwrite(new_path, rotated)
    
    rotated = ndimage.rotate(src, 180)
    new_filename=filename.replace('.jpg', '-rot-180.jpg')
    new_path = f'{data_set}{new_filename}'
    print(new_path)
    cv2.imwrite(new_path, rotated)
    
    rotated = ndimage.rotate(src, 90)
    new_filename=filename.replace('.jpg', '-rot-270.jpg')
    new_path = f'{data_set}{new_filename}'
    print(new_path)
    cv2.imwrite(new_path, rotated)
    

    
 


