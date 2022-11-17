#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar  8 14:04:15 2022

@author: lucas
"""

"""Diagrama fundamental (funcion graficadora). Recibe el df,tamaño de ventana, 
la distancia maxima hasta donde dibuja  
y nombre de archivo de salida. """



import pandas as pd
import matplotlib.pyplot as plt
import numpy as np



def dibujar_diagrama_fundamental(df,max_dist,t_ventana,is_density=False):
    
    
    fig,ax = plt.subplots()

    df = df.sort_values("Dist_Closest")
    
    df_finito = df[df["Dist_Closest"]<max_dist]
    
   
    
    distancias = df_finito["Dist_Closest"]
    velocidades = abs(df_finito["Velocidad"])


###ventana desliante grupo
    i = 0
    distancias_marcadas = []
    velocidades_promedio = []
    desvios = []
    if is_density:
        densidad = [1/x for x in distancias[len(distancias)-1:0:-1]]
        velocidades = velocidades[len(velocidades)-1:0:-1]
        while( i+t_ventana < len(densidad) ):
            sub_vel = velocidades[i:i+t_ventana]
            velocidades_promedio.append(np.mean(sub_vel))
            distancias_marcadas.append((np.mean(densidad[i:i+t_ventana]) ) )
            i = i+1    
        ax.plot(distancias_marcadas,velocidades_promedio)
        plt.semilogy()
        ax.set_xlabel(r"Density ($1/\mu$m)",fontsize=14)
         
        
        
        
    else:
        while( i+t_ventana < len(distancias) ):
            sub_vel = velocidades[i:i+t_ventana]
            velocidades_promedio.append(np.mean(sub_vel))
            distancias_marcadas.append((np.mean(distancias[i:i+t_ventana]) ) )
            i = i+1    
        ax.plot(distancias_marcadas,velocidades_promedio)
        
        ax.set_xlabel(r"Distance to Closest ($\mu$m)",fontsize=14)
    
    ax.set_ylabel(r"Velocity ($\mu$m/min)",fontsize=12)
    plt.grid()
    # plt.legend()
  
    # fig.savefig(output,bbox_inches="tight",dpi=250)
    # plt.close(fig)

    return (fig)











# def dibujar_diagrama_fundamental_(df,max_dist,t_ventana,output,is_density=False):
    
    
#     fig,ax = plt.subplots()

#     df = df.sort_values("Dist_Closest")
    
#     df_finito = df[df["Dist_Closest"]<max_dist]
    
#     df_finito_tren = df_finito[df["Agrupada"]]
#     df_finito_sola = df_finito[df["Agrupada"]==False]
    
#     distancias_tren = df_finito_tren["Dist_Closest"]
#     velocidades_tren = abs(df_finito_tren["Velocidad"])

#     distancias_sola = df_finito_sola["Dist_Closest"]
#     velocidades_sola = abs(df_finito_sola["Velocidad"])

# ###ventana desliante grupo
#     i = 0
#     distancias_marcadas = []
#     velocidades_promedio = []
#     desvios = []
        
#     while( i+t_ventana < len(distancias_tren) ):
#         sub_vel = velocidades_tren[i:i+t_ventana]
#         velocidades_promedio.append(np.mean(sub_vel))
#         distancias_marcadas.append((np.mean(distancias_tren[i:i+t_ventana]) ) )
#         i = i+1    
#     ax.plot(distancias_marcadas,velocidades_promedio,"green",label="Grouped")
    

# ###ventana desliante isolated
#     #ancho_ventana = 100
#     i = 0
#     distancias_marcadas = []
#     velocidades_promedio = []
#     desvios = []
    
#     while( i+t_ventana < len(distancias_sola) ):
#         sub_vel = velocidades_sola[i:i+t_ventana]
#         velocidades_promedio.append(np.mean(sub_vel))
#         distancias_marcadas.append((np.mean(distancias_sola[i:i+t_ventana])) )
#         i = i+1
    
#     ax.plot(distancias_marcadas,velocidades_promedio,"blue",label="Isolated")
#     ax.set_xlabel(r"Distance to Closest ($\mu$m)",fontsize=14)
#     ax.set_ylabel(r"Velocity ($\mu$m/min)",fontsize=12)
  
#     plt.grid()
#     plt.legend()
  
#     fig.savefig(output,bbox_inches="tight",dpi=250)
#     plt.close(fig)

