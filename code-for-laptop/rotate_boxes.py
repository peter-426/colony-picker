# -*- coding: utf-8 -*-
"""
Created on Fri Aug 27 17:18:09 2021

used to verify that the rotated boxes coincide with rotated colony locations

"""

import os

class Point:  
    x=0
    y=0
    
    def __init__(self, x,y):
        self.x=x
        self.y=y


data_set = 'images-rot/'

class_names = ['car']



def rot_row(line, rot_ext, angle):
    fields = line.split(",")
            
    rot_name=fields[0].replace(".jpg", rot_ext)
    print(line, end="")
    
    xmin=int(fields[4]); ymin=int(fields[5])
    xmax=int(fields[6]); ymax=int(fields[7])
         
    new_min_pt = Point(0,0)    
    new_max_pt = Point(0,0)

        
    if angle == 90:
      new_min_pt.x= 1600-ymin
      new_min_pt.y= xmin
      new_max_pt.x= 1600-ymax
      new_max_pt.y= xmax
      
      min_x=new_min_pt.x
      min_y=new_min_pt.y
      max_x=new_max_pt.x
      max_y=new_max_pt.y
      
    if angle == 180:
      new_min_pt.x= 1600-ymin
      new_min_pt.y= xmin
      new_max_pt.x= 1600-ymax
      new_max_pt.y= xmax
      
      min_x = 1600- new_min_pt.y
      min_y= new_min_pt.x
      max_x= 1600- new_max_pt.y
      max_y=  new_max_pt.x
      
    if angle == 270:
      new_min_pt.x= ymin
      new_min_pt.y= 1600-xmin
      new_max_pt.x= ymax
      new_max_pt.y= 1600-xmax
      
      min_x=new_min_pt.x
      min_y=new_min_pt.y
      max_x=new_max_pt.x
      max_y=new_max_pt.y
    
    
    new_line= ",".join([rot_name,fields[1],fields[2],fields[3],\
                        str(min_x), str(min_y), str(max_x), str(max_y)])
    print(new_line, "\n")
    return new_line



files = os.listdir(data_set)

for filename in files:
    if not filename.endswith(".csv"):
        continue
    
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
        
f2= open(data_set + filename_rot, "w") 
f2.writelines(new_lines)
f2.close()
            
            
            
            
            