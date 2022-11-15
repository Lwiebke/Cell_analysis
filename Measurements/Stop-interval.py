#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr  6 17:33:18 2022

@author: lucas
"""


"""Esta funcion busca los puntos de stop de las particulas (momentos cercanos a 0) y separa a la misma en intervalos.

    Need revision """


def calcular_intervalos(df):
    
    df["Intervalo_n"] = [0]*df.shape[0]
    df["Sentido"] = ["0"]*df.shape[0]
    
    for id_part, part in df.groupby("ID"):
        part.sort_values("Time")
        
        t = list(part["Time"])
        v = list(part["Velocidad"])
        
        v_comparar = v[0]
        contador_intervalos = 1
        #print("Celula ID: " + str(id_part))
        if v_comparar > 0:
            tipo_int = "+"
        else:
            tipo_int = "-"
        
        i = 0
        while i  < len(t):
            while(v[i]*v_comparar > 0 and i  < len(t)-1):
            
                part.loc[part["Time"]==t[i],"Intervalo_n"]=contador_intervalos
                part.loc[part["Time"]==t[i],"Sentido"]=tipo_int
                i += 1
            

            #print("Intervalos para la celula: "+ str(id_part)+ " "+ str(contador_intervalos))
            v_comparar = v[i]
            if v_comparar > 0:
                tipo_int = "+"
            else:
                tipo_int = "-"
            i+=1
            contador_intervalos+=1
            
        df.loc[df["ID"]==id_part,"Intervalo_n"]=part["Intervalo_n"]      
        df.loc[df["ID"]==id_part,"Sentido"]=part["Sentido"]
  
    return df
    