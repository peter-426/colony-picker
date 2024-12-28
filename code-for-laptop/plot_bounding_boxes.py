#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from PIL import Image


image_set="images-rot/"
image_filename= image_set + "img_2021-08-25_16-43-48-rot-270.jpg"

    

fn = os.path.basename(image_filename)

train_labels_filename = image_set + "labels-rot.csv"  # train_labels.csv

im = Image.open(image_filename)

# Create figure and axes
fig, ax = plt.subplots()

# Display the image
ax.imshow(im)

label_file = open(train_labels_filename, 'r')

line = label_file.readline()

while (line):
    if line.startswith(fn):
        fields=line.split(',')
        (xmin, ymin, xmax, ymax) =  int(fields[4]), int(fields[5]), int(fields[6]), int(fields[7])
        width=xmax-xmin
        height=ymax-ymin

        # make and draw rectangle 
        rect = patches.Rectangle((xmin,ymin), width, height, linewidth=1, edgecolor='b', facecolor='none')   
        ax.add_patch(rect)

    line = label_file.readline()

plt.xlabel("x")
plt.ylabel("y")
plt.title(image_filename)
plt.show()


fig.savefig(fn+"-boxes.jpg")

