#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul  2 11:07:26 2021

@author: lucas
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
import sys

""" Path to the Cell_analysis directory"""
sys.path.append('../')


from Cell_analysis.Experiment import Experiment


from Cell_analysis.Preprocessing.Formatter import get_calibrated
from Cell_analysis.Preprocessing.Velocity import *
from Cell_analysis.Preprocessing.Channels import asignar_canales, asignar_canales_dbscan, plot_channels



""" 
    This script prepares the data for further analysis. The inputs are:
        A file with the tracked cells, in pixel units
        A metadata file, from where it takes the pixel size and time frame
        An extra file, used to find the other 2 files.
    
"""



input_path = "./"

experimentos=[]



datafiles = ["30um_data"]
for f in datafiles:
    exp = Experiment(f)
    experimentos.append(exp)



print("Cargando datos y calculando cosas... ... ")
all_data = {}
   
for k in range(len(experimentos)):    
    
    experimento = experimentos[k]
    all_data[experimento.name] = get_calibrated(input_path+experimento.file, input_path+experimento.metadata)
    df = all_data[experimento.name]
    
    df["Canal"] = np.zeros(df.shape[0])
    df['Position X'] = df['Position X'].astype(float)
    df['Position Y'] = df['Position Y'].astype(float)

    """ Asignar canales """


    """ when using dbscan, always check the channels plot to verify the channels.
    Sometimes it needs to be calibrated"""
    
    dist = 20
    df =  asignar_canales_dbscan(df,dist,2)
    
    plot_channels(df)
        
    df = velocidad_2d(df)
    df["Time"] = round(df["Time"],2)
    

    df.to_csv(experimento.name+"_procesado.csv",index=False)
    # all_data[experimento] = df

        






