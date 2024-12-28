
from opentrons.simulate import simulate, format_runlog

import sys


'''
with open(out_folder + '/' + 'centers.txt', 'w') as f:
    for item in center_list:
        f.write("%d,%d\n" % (item[0], item[1]))
'''
 
out_folder='data'

lines=[]
with open(out_folder + '/' + 'centers.txt',) as f:
    lines = [line.rstrip() for line in f]

wt_list=[1,2,3]
mut2_list=[4,5,6]

print('wt colony centers\n')

for ii in wt_list:   
  xy=lines[ii].split(',')  
  x=int(xy[0])
  y=int(xy[1])  
  print(f'coords x={x}, y={y}')


print('\n\nmut2 colony centers\n') 
for ii in mut2_list:   
  xy=lines[ii].split(',')  
  x=int(xy[0])
  y=int(xy[1])  
  print(f'coords x={x}, y={y}')