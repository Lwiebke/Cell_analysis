#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 22 08:36:43 2022

@author: lucas
"""

"""Script to adapt the output of the cell finder and prepare for later analysis"""



import pandas as pd
#import copy


def get_calibrated(filename,metadata_file):

    with open(metadata_file) as meta:
        info = meta.readlines()
        pixel_width = float(info[0].split(" ")[2]) 
        pixel_height = float(info[1].split(" ")[2])
        time_interval = float(info[2].split(" ")[2])
        
    data_positions = pd.read_csv(filename,header=None,names=["Frame","Position Y","Position X","ID"])
    #data_positions = copy.deepcopy(data_pixel)
    data_positions["Position Y"] = data_positions["Position Y"]*pixel_height
    data_positions["Position X"] = data_positions["Position X"]*pixel_width
    
    ## To express all measures in minutes (micrometers per minute is commonly used)
    data_positions["Time"] = (data_positions["Frame"]*time_interval)/60
    
    return data_positions



