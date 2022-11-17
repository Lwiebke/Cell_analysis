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



sys.path.append('/home/lucas/Escritorio/Analisis-datos/testeo/')


from Cell_analysis.Preprocessing.Formatter import get_calibrated
from Cell_analysis.Preprocessing.Neighbour import find_neig, set_agrupada_o_aislada
from Cell_analysis.Preprocessing.Velocity import *
from Cell_analysis.Preprocessing.Channels import asignar_canales, asignar_canales_dbscan, plot_channels


from Cell_analysis.Experiment import Experiment
from Cell_analysis.Measurements.Train_ID_finder import definir_trenes

results_path = "./"



experimentos=[]

datafiles = ["exp_6um_data","exp_6um_rep1_data","exp_6um_rep2_data"]


for f in datafiles:
    exp = Experiment(f)
    experimentos.append(exp)


# experimentos.append("6um")

d_cut = 30


print("Cargando datos y calculando cosas... ... ")
all_data = {}
   
for k in range(len(experimentos)):    

    
    experimento = experimentos[k]
    all_data[experimento.name] = get_calibrated(experimento.file, experimento.metadata)
    df = all_data[experimento.name]
    
    df["Canal"] = np.zeros(df.shape[0])
    df['Position X'] = df['Position X'].astype(float)
    df['Position Y'] = df['Position Y'].astype(float)
    
    
    
    """ Asignar canales """
    df =  asignar_canales(df,experimento.n_canales,experimento.pendiente)
    # df =  asignar_canales_dbscan(df)
    
    plot_channels(df)
    
    
    
    df = velocidad_instantanea_1D(df)
    df = find_neig(df)
    """Aca para la velociadad relativa a la vecina mas cercana """
    # df = calcular_vel_vecina(df)
    df = set_agrupada_o_aislada(df,d_cut)
    
    df["Distancia_adelante"] = np.where(
                            df['Velocidad'] < 0 , df["Dist_izquierda"], np.where(
                            df['Velocidad'] > 0, df["Dist_derecha"] ,None)) 

    df = definir_trenes(df,d_cut)
    df = df.sort_values("Time")
    
    print("")
    print(experimento)
    print("")
    
    df["Time"] = round(df["Time"],2)
    
    # df=df.loc[:,["ID","Canal"]]
    
    df.to_csv(experimento.name+"_procesado.csv",index=False)
    all_data[experimento] = df
    
            






