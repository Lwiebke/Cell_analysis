#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 20 11:37:51 2022

@author: lucas
"""




class Experiment:

    """ This class keeps needed information about experiments. Its used to find the files, and when needed, align the channels with
    the X axes befor assigning the channels """

    
    def __init__(self,exp_data_filename):
        
        with open(exp_data_filename) as data:
            info = data.readlines()
            # print(info)
            self.name = (info[0].split(":")[1])[:-1]
            self.file = (info[1].split(":")[1])[:-1]
            self.metadata = (info[2].split(":")[1])[:-1]
            
            self.n_canales = int(info[3].split(":")[1])
            self.pendiente = float(info[4].split(":")[1])
            
            # self.blobs_dir = (info[5].split(":")[1])[:-1]
            # self.blob_file = (info[6].split(":")[1])[:-1]
            
            
        