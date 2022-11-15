#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 26 10:20:38 2022

@author: lucas
"""
import copy 

def calcular_vel_vecina(df):
    
    df["Velocidad_a_vecina"]=0
    for id_cell, cell in df.groupby("ID"):
        vel_relativa = [0]*cell.shape[0]
        cell.sort_values("Time")
        tiempos = list(cell["Time"])
        for i,t in enumerate(tiempos[:-1]):
            vel_relativa[i] = float(cell.loc[cell["Time"]==tiempos[i+1],"Dist_Closest"]) -float( cell.loc[cell["Time"]==t,"Dist_Closest"])
        
        df.loc[df["ID"]==id_cell,"Velocidad_a_vecina"]=copy.deepcopy(vel_relativa)

    return df        