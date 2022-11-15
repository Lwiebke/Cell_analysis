#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep  8 11:26:30 2022

@author: lucas
"""

import numpy as np
#import
from scipy.ndimage import gaussian_filter1d




def find_colisiones(df, d_cut, dt):
    # m representa el numero de pasos que corresponden a 1.5 minutos sin importar el timestep
    m = int(round( 2/dt + 0.5))
    
    # print("Para la colision se usaron: " +  str(m) + " pasos anteriores")
#    m = 4
    df["Colision"]=[False]*df.shape[0]
    df = df.sort_values("Time")
    
    
    for id_p, particle_data in df.groupby("ID"):
        tiempos = list(particle_data["Time"])
#        d_mins = list(particle_data["Dist_Closest"])
        d_izq = list(particle_data["Dist_izquierda"])
        d_der = list(particle_data["Dist_derecha"])
        dist_delante = [0]*len(tiempos)
        vels = list(particle_data["Velocidad"])
        for i in range(len(vels)):
            if vels[i] <= 0:
                dist_delante[i] = d_izq[i]
            else:
                dist_delante[i] = d_der[i]

        #print(len(tiempos))
        if (len(tiempos) > m):
        
            for it, t in enumerate(tiempos[0:-m], start = m):
                if  dist_delante[it] < d_cut:
                    count = 0
                    #preguntar por los m isntantes anteriores:
                    for ind_ant in range(-m,0,1):
                        if dist_delante[it+ind_ant] >= d_cut:
                            count += 1

                    if count == m:
                        
                        indice = particle_data[particle_data["Time"]==tiempos[it]].index
                        df.loc[indice,"Colision"]=True
 

    """ Post procesamiento de colisiones"""
    colis = df.loc[df["Colision"],]
    for ss, col in colis.groupby(["Time","Canal"]):
        if col.shape[0]  != 2: # Hasta aqui significa que la colision fue encontrada en 2 a la vez.
            df.loc[ (df["Time"]==ss[0]) & (df["Canal"] == ss[1]) ,"Colision"] = False
            
        if col.shape[0] == 2:
            
            par = list(col["ID"])
            if ( abs(col.loc[col["ID"] == par[0],"Position X"].item() - col.loc[col["ID"] == par[1],"Position X"].item()) > 80 ):
                df.loc[ (df["Time"]==ss[0]) & (df["Canal"] == ss[1]) ,"Colision"] = False
            
             #            col[]
            
    
#    df[df["Colision"]]==colis
   
    
    return(df)
#                    





def find_collision_end(df,dt):
    
  
    tiempo_usado_colision = 2
    m = int(round( tiempo_usado_colision/dt )+0.5)
    
    """ promediar velocidades"""
    



    df["Collision_solved"] = False
    n_steps_3_mins = int( round( 3/dt )+0.5)
    lista = []
    # print("Se usan " + str(n_steps_3_mins)+ " pasos rectos para resolver colision")
    for ID, part in df.groupby("ID"):
        if (any(part["Colision"])):
            # print(str(ID)+ " tiene colision")
            vel = part["Velocidad"]
            
            # vel = gaussian_filter1d(vel, 100)
            
            # df.loc[df["ID"]==ID,"Velocidad"] = vel
        
             
            times = list(part["Time"]) 
            t_cols = part.loc[part["Colision"],"Time"]
            for col_time in t_cols:
                # print("colision en " + str(col_time) )
                """ Contaré como resuelta la colision cuando haya 3 minutos de velocidad alta ininterrumpidos"""
                velocidades_a_estudiar = list(part.loc[part["Time"] > col_time, "Velocidad"])
                mean_previa = np.mean(list(part.loc[part["Time"] < col_time, "Velocidad"])) 
                col = len(vel)-len(velocidades_a_estudiar)
                # velocidades_a_estudiar = velocidades_a_estudiar[m:]
                aux = 0
                fin = len(velocidades_a_estudiar)-1
                for i, v in enumerate(velocidades_a_estudiar[:-n_steps_3_mins],start = 0):
                    # if ( (velocidades_a_estudiar[i] * velocidades_a_estudiar[i-1]) > 0 ):# and(abs(v) > 0.66*mean_previa) :
                    if (abs(np.mean(velocidades_a_estudiar[i : i+n_steps_3_mins])) > 5  and  ( (velocidades_a_estudiar[i] * velocidades_a_estudiar[i-1]) > 0 )):
                        aux += 1
                    else:
                        aux=0
                    if (aux == n_steps_3_mins):
                        #fin = i - int(n_steps_3_mins)
                        fin = i - int(n_steps_3_mins/2)
                        break
                    
                
                if (fin != len(velocidades_a_estudiar)-1):
                    df.loc[ (df["ID"]==ID) & (df["Time"] == times[col+fin]),"Collision_solved"] = True
    
    return(df)






def calculate_col_time(df,d_cut):

        

    dt = min(list(df["Time"]))

    df = find_colisiones(df,d_cut,dt)
    df = find_collision_end(df,dt)
    
    duraciones_colision = []
    
    for id_p, part in df.groupby("ID"):
         if (any(part["Colision"])): #tiene inicio de colision
             tiempos_col = list(part.loc[part["Colision"],"Time"])
             tiempos_sol = list(part.loc[part["Collision_solved"],"Time"])
             for i, t in enumerate(tiempos_sol):
                 duracion = tiempos_sol[i] - tiempos_col[i]
                 duraciones_colision.append(duracion)                 
                 # if (any(part["Collision_solved"])): # y tiene fin de colision
                      
    return(duraciones_colision)






























    
            