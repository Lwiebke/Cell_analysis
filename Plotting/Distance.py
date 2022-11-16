#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 31 15:17:19 2022

@author: lucas
"""




import matplotlib.pyplot as plt
import numpy as np


def draw_distance_vs_time(df,dcut,path):

    for id_p, particle_data in df.groupby("ID"):
        distancia_izq = np.array(list(particle_data["Dist_izquierda"]))
        distancia_der = list(particle_data["Dist_derecha"])
        time=list(particle_data["Time"])
        fig=plt.figure()
        
        id_vec = list(set(particle_data.loc[particle_data["Vecino_izq"].notnull(),"Vecino_izq"]))
        if id_vec:
            plt.plot(time,-1*distancia_izq, ".-r",label="Left cell: "+str(int(id_vec[0])) )
        
        
        id_vec = list(set(particle_data.loc[particle_data["Vecino_der"].notnull(),"Vecino_der"]))
        if id_vec:
            plt.plot(time, distancia_der, ".-g",label="Right cell: "+str(int(id_vec[0])))
        plt.plot((time),[0]*len(time), ":k", label=None) #r"$Cell:$")
        
        plt.xlabel("Time (min)",fontsize=17)
        plt.ylabel(r"Distance to neighbour ($\mu$m)",fontsize=17)
        plt.fill_between(time,[-dcut]*len(time),[dcut]*len(time),alpha=0.25,label="Contact Zone")
        plt.legend()
        fig.savefig(path + "distance_"+str(id_p)+".png",bbox_inches="tight",dpi=200)
        plt.close()