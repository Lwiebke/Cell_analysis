#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 16 11:54:43 2022

@author: lucas
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

import sys

""" Path to the Cell_analysis directory"""
sys.path.append('/home/lucas/Escritorio/Analisis-datos/testeo/')


from Cell_analysis.Measurements.Collisions import * 
from Cell_analysis.Measurements.Relative_speed import * 

from Cell_analysis.Plotting.Animar import *
from Cell_analysis.Plotting.Distance import *
from Cell_analysis.Plotting.Fundamental_Diagram import *
from Cell_analysis.Plotting.Position_velocity import *


all_data = {}

nombre = "6um-rep1_procesado.csv"
experimento = "6um-20s"

df = pd.read_csv(nombre)
path_result = "./"
d_cut = 30
 


" Here we serach colisions and calculate the time they take to get solved"
# df, t_col = calculate_col_time(df,d_cut) 



""" Fast visualization to see every trayectory and velocity. Option to show automatic collisons found.

plot_pos_by channel is specially usefull to check for missasigned colisions"""
# plot_pos_n_vel(df,path_result,show_colision=True)
# plot_pos_by_channel(df,path_result,show_colision=True)


""" Animation can be made with 2 options, Y position or just by channel """

# anim_1d = animar_1D(df)
# anim_1d.save("anim1d.gif",dpi=300)

anim_2d = animar_2D(df)
anim_2d.save("anim2d.gif",dpi=300)


""" Diagrama Fundamental """
max_dist = 600
sliding_window = 75

fig = dibujar_diagrama_fundamental(df,max_dist,sliding_window,is_density=False)

fig.savefig("Fundamental_diagram_"+experimento+".png",dpi=300,bbox_inches="tight")


""" Plots de cada célula y las distancias a sus vecinos """
contact_distance=30
draw_distance_vs_time(df,contact_distance,path_result)




""" PDF de distancias y velocidades  (simple) )"""
distancias_menores_40 = (list(df[df["Dist_Closest"] < 40]["Dist_Closest"]))
fig = plt.figure()
maxima_distancia = max(distancias_menores_40)
bins=30
pdf, bin_loc = np.histogram(distancias_menores_40, bins, range = (0,maxima_distancia), density = True)
plt.plot( bin_loc[:-1], pdf, ".-",lw = 1 )
plt.xlabel(r"Distance to closest ($\mu$m)",fontsize = 12)
plt.ylabel(r"PDF ",fontsize = 12)
plt.grid()

fig.savefig("PDF_Distances"+str(experimento)+".png",dpi=300,bbox_inches="tight")
fig.clear()






""" To compare diferent experiments """



files = ["6um_procesado.csv","6um-rep1_procesado.csv","6um-rep2_procesado.csv",]
experimentos = ["6um","rep1","rep2"]

for i,arch in enumerate(files):
    all_data[experimentos[i]] = pd.read_csv(files[i])

distancias_menores_40 = []
velocidades_totales = []
rapidez_totales = []

for experimento in all_data.keys():        
    df=all_data[experimento]
    distancias_menores_40.append(list(df[df["Dist_Closest"] < 40]["Dist_Closest"]))
    rapidez_totales.append(list(abs(df[abs(df["Velocidad"]) < 50]["Velocidad"])))
    



"""Distance"""


fig = plt.figure()
fig.clear()
# exp = (distancias_menores_40[0])
maxima_distancia = max(max(distancias_menores_40))
bins = 22
for k in range(len(experimentos)): 
  
    exp = distancias_menores_40[k]
    exp_pdf, bin_loc = np.histogram(exp, bins, range = (0,maxima_distancia), density = True)
    plt.plot( bin_loc[:-1], exp_pdf, "-",marker="." , label = experimentos[k],lw = 0.75,alpha=1)        
plt.legend()
plt.xlabel(r"Distance to closest ($\mu$m)",fontsize = 12)
plt.ylabel(r"PDF ",fontsize = 12)
plt.grid()
fig.savefig("PDF_Distances.png",dpi=300,bbox_inches="tight")
fig.clear()


""" Speed """
fig = plt.figure()
fig.clear()
# exp = (rapidez_totales[0])
maxima_distancia = max(max(rapidez_totales))
bins = 12
for k in range(len(experimentos)): 
  
    exp = rapidez_totales[k]
    exp_pdf, bin_loc = np.histogram(exp, bins, range = (0,maxima_distancia), density = True)
    plt.plot( bin_loc[:-1], exp_pdf, "-",marker="." , label = experimentos[k],lw = 0.75,alpha=1)        
plt.legend()
plt.xlabel(r"Speed ($\mu$m/min)",fontsize = 12)
plt.ylabel(r"PDF ",fontsize = 12)
plt.grid()
fig.savefig("PDF_speed.png",dpi=300,bbox_inches="tight")
fig.clear()







