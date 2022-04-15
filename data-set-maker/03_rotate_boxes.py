# -*- coding: utf-8 -*-
"""
Created on Fri Aug 27 17:18:09 2021

This is Step 3:
rotated bounding boxes to coincide with rotated colony locations

Step 4 will be to norm and format for tflite
$ norm_coords_and_format.py  > train_labels-normed.csv

"""

import os

class Point:  
    x=0
    y=0
    
    def __init__(self, x,y):
        self.x=x
        self.y=y


data_set = 'data-set-maker/images-25-26-orange-white/train/'


def rot_row(line, rot_ext, angle):
    fields = line.split(",")
            
    rot_name=fields[0].replace(".jpg", rot_ext)
    #print(line, end="")
    
    xmin=int(fields[4]); ymin=int(fields[5])
    xmax=int(fields[6]); ymax=int(fields[7])
              
    if angle == 90:
      min_x= ymin
      max_x= ymax
      
      min_y= 1600-xmax
      max_y= 1600-xmin
      
    if angle == 180:
      min_x= 1600-xmax
      max_x= 1600-xmin
            
      min_y= 1600-ymax
      max_y= 1600-ymin
      
    if angle == 270:
      min_x= 1600-ymax
      max_x= 1600-ymin
            
      min_y= xmin
      max_y= xmax
          
    ##########################################################################
    ## The bounding box is defined by it's upper left and lower left
    ## coordinated where pt (0,0) is the upper left corner of an image.
    #
    ## Rotation will change the relative coordinates, e.g. after rotating  
    # min_x should be less that max_x, same for min_y versus max_y
    ##########################################################################
    assert min_x < max_x, f"bounding boxes rotation error: {angle}"
    assert min_y < max_y, f"bounding boxes rotation error: {angle}"  
       
    new_line= ",".join([rot_name,fields[1],fields[2],fields[3],\
                        str(min_x), str(min_y), str(max_x), str(max_y)])
    print(new_line, "\n")
    return new_line



# files = os.listdir(data_set)

# for filename in files:
#     if not filename.endswith(".csv"):
#         continue
   
filename="train_labels_orange_white.csv"
    
print(filename)
filename_rot = filename.replace(".csv", "-rot.csv")

new_lines=[]

with open(data_set + filename, "r") as f:
    line = f.readline()
    print(line)  # header
    line = f.readline()
    while line.startswith("img_"):
        new_lines.append(line)
        new_lines.append(rot_row(line, "-rot-90.jpg",   90) + "\n")
        new_lines.append(rot_row(line, "-rot-180.jpg", 180) + "\n")
        new_lines.append(rot_row(line, "-rot-270.jpg", 270) + "\n")
            
        line = f.readline()
        
        
###################################################        
f2= open(data_set + filename_rot, "w") 
f2.writelines(new_lines)
f2.close()
###################################################
            
            
            
            
            