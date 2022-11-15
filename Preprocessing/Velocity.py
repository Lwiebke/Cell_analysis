#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 28 11:46:36 2022

@author: lucas
"""

""" Different ways of calculating speed. It can be instantaneous or using a window, and also 1D or 2D """

#import sys

def velocidad_instantanea_1D(df,experimento):
    
    df["Velocidad"]=[0]*df.shape[0]
    for part_id, particula in df.groupby("ID"):
        particula=particula.sort_values("Time")
        v = []
        tiempos = list(particula["Time"]) 
        #print(len(tiempos))
        if len(tiempos)>2:
            for j, t  in enumerate(tiempos):
                if j < len(tiempos)-1:
                    #print(float(particula[particula["Time"] == tiempos[j+1]]["Position X"]))
                    #sys.exit()
                    insta_vel = ( (float(particula[particula["Time"] == tiempos[j+1]]["Position X"]) - float(particula[particula["Time"] == t]["Position X"]) ) 
                                    / (tiempos[j+1] - tiempos[j]) ) 
                    
                    v.append(insta_vel)
                
                else:
                    v.append(float('NaN'))
        else:
            v=[float('NaN')]*len(tiempos)
    
        
        particula["Velocidad"] = v 
        df[df["ID"] == part_id] = particula 

    return(df)
    



def velocidad_time_w_1D(df):
    
    times = list(set(df["Time"]))
    times.sort()
    dt = times[1]-times[0]
    
    pasos_X_min = int( round( 1/dt + 0.5 ) )
    
            
    df["Velocidad"]=[0]*df.shape[0]
    for part_id, particula in df.groupby("ID"):
        particula=particula.sort_values("Time")
        v = []
        tiempos = list(particula["Time"]) 
        #print(len(tiempos))
        # if len(tiempos) > 2*pasos_X_min:
        for j, t  in enumerate(tiempos):
            if j < len(tiempos)-pasos_X_min:
                #print(float(particula[particula["Time"] == tiempos[j+1]]["Position X"]))
                #sys.exit()
                insta_vel = ( (float(particula[particula["Time"] == tiempos[j+pasos_X_min]]["Position X"]) - float(particula[particula["Time"] == t]["Position X"]) ) 
                                / (tiempos[j+pasos_X_min] - tiempos[j]) ) 
                        
                v.append(insta_vel)
            
            else:
                v.append(float('NaN'))
        # else:
        #     v=[float('NaN')]*len(tiempos)
    
        

        df.loc[df["ID"] == part_id,"Velocidad"] = v

    return(df)
    


def velocidad_2d(df):
    import numpy as np
    
    times = list(set(df["Time"]))
    times.sort()
    dt = times[1]-times[0]
    
    pasos_X_min = int( round( 1/dt + 0.5 ) )
    
    
        
    df["Velocidad"]=[float('NaN')]*df.shape[0]
    df["Dir_vel"]=[float('NaN')]*df.shape[0]
    for part_id, particula in df.groupby("ID"):
        particula=particula.sort_values("Time")
        v = []
        direc = []
        tiempos = list(particula["Time"]) 
        #print(len(tiempos))
        # if len(tiempos) > 2*pasos_X_min:
        for j, t  in enumerate(tiempos):
            if j < len(tiempos)-pasos_X_min:
                #print(float(particula[particula["Time"] == tiempos[j+1]]["Position X"]))
                #sys.exit()
                pos_x_fin = float(particula[particula["Time"] == tiempos[j+pasos_X_min]]["Position X"])
                pos_y_fin = float(particula[particula["Time"] == tiempos[j+pasos_X_min]]["Position Y"])
                
                pos_x_ini = float(particula[particula["Time"] == tiempos[j]]["Position X"])
                pos_y_ini = float(particula[particula["Time"] == tiempos[j]]["Position Y"])                    
                
                d = np.sqrt( (pos_x_fin-pos_x_ini)**2 + (pos_y_fin-pos_y_ini)**2 ) 
                insta_vel =  d / (tiempos[j+pasos_X_min] - tiempos[j]) 
                v.append(insta_vel)
                d = np.arctan2(pos_y_fin-pos_y_ini,pos_x_fin-pos_x_ini)
                direc.append(d)
            else:
                v.append(float('NaN'))
                direc.append(float('NaN'))
        # else:
        #     v = [0]*len(tiempos)
        #     d = [0]*len(tiempos)
    
        df.loc[df["ID"] == part_id,"Velocidad"] = v
        df.loc[df["ID"] == part_id,"Dir_vel"] = d
        

    return(df)
    





