
# date: 2021/2022
# author: Peter Hebden, phebden@gmail.com

import re
import os
import random
from shutil import copyfile

# https://www.tensorflow.org/lite/tutorials/model_maker_object_detection
# https://cloud.google.com/vision/automl/object-detection/docs/prepare
# The labels must be valid strings (no comma inside). The comma is only 
# an issue in CSV-based importing. A way to address this issue is: 
# "file_comma,path","label,comma",0,0,,,1,1,,
#  box coordinates are upper left pt, lower right pt

# norm coords by img size and put xmin,ymin, xmax,ymax in right format

src_folder = 'images-25-26-orange-white/train/'
dest_folder= 'images-25-26-orange-white/test/'

if not os.path.exists(dest_folder):
    os.makedirs(dest_folder)

src_file = 'images-25-26-orange-white/train/train_labels_orange_white-rot.csv'
dest_file= 'images-25-26-orange-white/train/train_labels-normed.csv'

src = open(src_file, 'r')
dest = open(dest_file, 'w')

lines=src.readlines()

#headings=lines[0];
#print(headings, "\n");

# one line per detected object (not per image)

prev_image = "xxx";
curr_image = "none";

for ii in range (len(lines)):
    if ii == 0:
        continue

    fields=lines[ii].split(",")
     
    width =int(fields[1]);
    height=int(fields[2]);  
    #print(" %d, %d \n" % (width, height));  
      
    # # normalize
    fields[4]= str(round(float(fields[4])/width,5));   # xmin
    fields[5]= str(round(float(fields[5])/height,5));  # ymin
    fields[6]= str(round(float(fields[6])/width, 5));  # xmax
    fields[7]= str(round(float(fields[7])/height,5));  # ymax
     
    line = ','.join([fields[0], fields[3], fields[4], fields[5], ',' , fields[6], fields[7]] );
    #print(line, "\n")
    curr_image = fields[0];  
    curr_image = re.sub("-rot-\d+","", curr_image)
    #print(curr_image, "\n")
      
    if (prev_image != curr_image):
        rand_num = random.random();
        if (rand_num < 0.90):
            dataset = "TRAIN"; 
        elif (rand_num < 0.96):
            dataset = "VALIDATION"; 
        else:
            dataset = "TEST";
            copyfile(src_folder + fields[0], dest_folder + fields[0])
            # for manual testing and visualisation
        
    prev_image = curr_image;
       	   
    # # TRAIN,filename.jpg,colony,0.5725,0.7708,,,0.6042,0.8017,,
    
    new_line = dataset + "," + line + ",,\n"
    dest.write(new_line);
    print(new_line)

src.close()
dest.close()
