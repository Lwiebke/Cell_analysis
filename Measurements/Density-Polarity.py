#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 19 14:29:46 2022

@author: lucas
"""

import numpy as np
import matplotlib.pyplot as plt


def calc_densisdad_por_canal(df):
    n_por_canal = {}
#    t_vistos = []
    times = list(set(df.Time))
    times.sort()
    for id_canal, canal in df.groupby("Canal"):
        if id_canal not in list(n_por_canal.keys()):
            n_por_canal[id_canal] = []
        canal.sort_values("Time")
        for t in times:
#            if t not in [t1[0] for t1 in n_por_canal[id_canal]]: 
            n_por_canal[id_canal].append(canal[canal["Time"]==t].shape[0])
            
            
    return n_por_canal
            
            
def polaridad_canal(df):
    pol_por_canal = {}
    for id_canal, canal in df.groupby("Canal"):
        if id_canal not in list(pol_por_canal.keys()):
            pol_por_canal[id_canal] = []
        canal.sort_values("Time")
        for t in list(canal.Time):
            hacia_derecha = canal[(canal["Time"]==t) & (canal["Velocidad"]>0)].shape[0]
            hacia_izquierda = canal[(canal["Time"]==t) & (canal["Velocidad"]<0)].shape[0]
            pol_por_canal[id_canal].append((t,(abs(hacia_derecha-hacia_izquierda)) / canal[canal["Time"]==t].shape[0]))            
    return pol_por_canal
    


def plot_dens_vs_rap(df, densidad_por_canal,exp):
    
#    medias_de_N=[]
    dens_media_por_canal = []
    rapidez_media_por_canal = []
    fig = plt.figure()
    for canal in densidad_por_canal.keys():
            
        datos_canal = densidad_por_canal[canal]
#        tiempos = [x[0] for x in datos_canal]
        N = [x[1] for x in datos_canal]
        
        dens_media_por_canal.append(np.mean(N))
        vels = [abs(x) for x in list(df.loc[df["Canal"]==canal, "Velocidad"])]
        rapidez_media_por_canal.append(np.mean(vels))
        
      
    plt.plot(dens_media_por_canal,rapidez_media_por_canal,"b.")
    plt.plot([min(dens_media_por_canal),max(dens_media_por_canal)],[np.mean(rapidez_media_por_canal),np.mean(rapidez_media_por_canal)],"k-")
    plt.plot([np.mean(dens_media_por_canal),np.mean(dens_media_por_canal)],[min(rapidez_media_por_canal),max(rapidez_media_por_canal)],"k-")
    
    plt.xlabel("Density (N cells)",fontsize=14)
    plt.ylabel(r"Speed ($\mu$m/min)",fontsize=14)
    plt.grid()
    
    
    
    fig.savefig("Dens_vs_vel-"+str(exp)+".png",dpi=300, bbox_inches="tight")
    

def plot_pol_vs_rap(df, pol_por_canal,exp):
    
#    medias_de_N=[]
    pol_media_por_canal = []
    rapidez_media_por_canal = []
    fig = plt.figure()
    for canal in pol_por_canal.keys():
            
        datos_canal = pol_por_canal[canal]
#        tiempos = [x[0] for x in datos_canal]
        N = [x[1] for x in datos_canal]
        
        pol_media_por_canal.append(np.mean(N))
        vels = [abs(x) for x in list(df.loc[df["Canal"]==canal, "Velocidad"])]
        rapidez_media_por_canal.append(np.mean(vels))
        
        
        
#    pol_media_por_canal = np.asarray(pol_media_por_canal)
#    rapidez_media_por_canal = np.asarray(rapidez_media_por_canal)
    print("is ploting")
    plt.plot(pol_media_por_canal,rapidez_media_por_canal,"b.")
    plt.plot([min(pol_media_por_canal),max(pol_media_por_canal)],[np.mean(rapidez_media_por_canal),np.mean(rapidez_media_por_canal)],"k-")
    plt.plot([np.mean(pol_media_por_canal),np.mean(pol_media_por_canal)],[min(rapidez_media_por_canal),max(rapidez_media_por_canal)],"k-")
    plt.xlabel("Polarity",fontsize=14)
    plt.ylabel(r"Speed ($\mu$m/min)",fontsize=14)
    plt.grid()
    
    
    
    fig.savefig("Pol_vs_vel-"+str(exp)+".png",dpi=300, bbox_inches="tight")
    
        
    
    



    
    
    