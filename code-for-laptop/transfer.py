#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# transfer.py
#
# Source tube_rack is 6 cols (1-6) by 4 rows (A-D) = 24 tubes.
# For each tube_rack, transfer vol ul per "well" to dest plate, 8 rows A-H
# Pools 1,2,3.   *** Uses 3 tips, 1 for each tube_rack. *** 
def transfer_24_to_96_batch(pipette, vol, tube_rack, plate_dest):
    counter=0
    num_racks = len(tube_rack)
    num_wells = len(tube_rack[0].wells())  #num wells per rack
    #print('\n\n num_wells = ', num_wells, '\n\n')
        
    for pool_idx in range(num_racks):
            pipette.transfer(vol,tube_rack[pool_idx].wells(),plate_dest.wells()[counter:counter+num_wells])  
            counter+=num_wells

# If 3 tube_racks, uses 3 x 24 = 72 tips, i.e. 1 per source "well".
def transfer_24_to_96(pipette, vol, tube_rack, plate_dest):
    counter=0
    num_racks = len(tube_rack)
    num_wells = len(tube_rack[0].wells())
        
    for pool_idx in range(num_racks):
        for ii in range(num_wells):
            pipette.transfer(vol, tube_rack[pool_idx].wells()[ii], plate_dest.wells()[counter])  
            counter+=1
 
def transfer_24_to_96_mix(pipette, vol, tube_rack, tube_rack_4, mix_reps, mix_vol):   
    counter = 0
    num_racks = len(tube_rack)
    num_wells = len(tube_rack[0].wells())

    for pool_idx in range(num_racks):
        for ii in range(num_wells):
            pipette.transfer(vol, tube_rack[pool_idx].wells()[ii], tube_rack_4.wells()[pool_idx])  
            counter+=1  
        pipette.pick_up_tip()
        pipette.mix(mix_reps, mix_vol, tube_rack_4.wells()[pool_idx] )
        pipette.blow_out()
        pipette.drop_tip()
          
def transfer_mix(pipette, vol, tube_rack_4, mix_reps, mix_vol):  
    counter = 0
    pool_72_idx = 3
    for pool_idx in range(3):
        pipette.transfer(vol, tube_rack_4.wells()[pool_idx], tube_rack_4.wells()[pool_72_idx])  
        counter+=1  
    # only 1 tube to mix, i.e. at pool_72_idx
    pipette.pick_up_tip()
    pipette.mix(mix_reps, mix_vol, tube_rack_4.wells()[pool_72_idx] )
    pipette.blow_out()
    pipette.drop_tip()
    
# transfer vol ul from tube_rack wells 1,2,3 tubes to the 96 well 
# plate destinations.  Source tube_rack column 1 = wells A1, B1, C1.
def transfer_rack_to_plate(pipette, vol, tube_rack, plate_dest):
    pipette.transfer(vol, tube_rack.wells()[0], plate_dest['A10'])  
    pipette.transfer(vol, tube_rack.wells()[0], plate_dest['B10'])      

    pipette.transfer(vol, tube_rack.wells()[1], plate_dest['C10'])  
    pipette.transfer(vol, tube_rack.wells()[1], plate_dest['D10']) 
    
    pipette.transfer(vol, tube_rack.wells()[2], plate_dest['E10'])  
    pipette.transfer(vol, tube_rack.wells()[2], plate_dest['F10']) 
