#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul  5 15:23:41 2022

@author: lucas
"""




import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


def plot_media_desvio(df,path, bool_plot):
    todas_velocidades = []
    vels_medias=[]
    desvios = []
   
    if bool_plot:    
        N = 0
        for id_part, part in df.groupby("ID"):
            if all(part["Agrupada"]==False):
                part.sort_values("Time")
                media = np.mean(list(part["Velocidad"]))
                desvio = np.std(list(part["Velocidad"]))
            #    paradas = list(part["Is_stop"])
                
            
                if part.shape[0]>20:
                    N += part.shape[0]        
                    vels_medias.append(media)
                    desvios.append( desvio)
                    todas_velocidades.append(np.asarray(list(part["Velocidad"])))
            #            for i, vel in enumerate(list(part["Velocidad"])):
            #                if abs(vel)<5 and abs(vel-media)>2*desvio:
            #                    paradas[i]=True
            
                   
                    fig = plt.figure()       
                    time=part["Time"]
                    plt.plot(part["Time"],part["Velocidad"],label=None)
                    plt.fill_between(time,[media-desvio]*len(time),[media+desvio]*len(time),alpha=0.25,color="b",label=r"1$\sigma$")
                    plt.fill_between(time,[media-2*desvio]*len(time),[media+2*desvio]*len(time),alpha=0.15,color="b",label=r"2$\sigma$")
                    plt.plot([min(list(part["Time"])),max(list(part["Time"]))],[media,media],"r",label="Mean")
                    plt.plot([min(list(part["Time"])),max(list(part["Time"]))],[0,0],"b:",label="Zero")
                    plt.xlabel("Time (min)",fontsize=14)
                    plt.ylabel(r"Speed ($\mu$m/min)",fontsize=14)
                    plt.legend()
                    fig.savefig(path+str(id_part)+".png",dpi=300,bbox_inches="tight")
                    
                    plt.close(fig)
                   
    else:
        N = 0
        for id_part, part in df.groupby("ID"):
            part.sort_values("Time")
            media = np.mean(list(part["Velocidad"]))
            desvio = np.std(list(part["Velocidad"]))
        #    paradas = list(part["Is_stop"])
            
        
            if part.shape[0]>20 and all(part["Agrupada"]==False):
                N += part.shape[0]        
                vels_medias.append(media)
                desvios.append( desvio)
                todas_velocidades.append(np.asarray(list(part["Velocidad"])))
      
    return((np.asarray(vels_medias), np.asarray(desvios)))
