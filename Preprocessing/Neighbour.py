#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 28 12:19:01 2022

@author: lucas
"""

""" Encontrar vecinos más cercanos, clasificarlos en delanteros o traseros 
dependiendo del sentido de la velocidad. Es importante porque sirve a la 
clasificación y a la distancia. """


def find_neig(df):
    df["Dist_Closest"]=float("inf")
    df["Dist_derecha"]=float("inf")
    df["Dist_izquierda"]=float("inf")
    df["Vecino_der"] = None
    df["Vecino_izq"] = None
    
    df = df.sort_values("Position X")
    df["ID"] = df["ID"].astype("int")
    
    for i, grp in df.groupby(["Canal","Time"]):
        if grp.shape[0] > 1:
            distancias = []
            closest = list(grp["Dist_Closest"])
            
            grp = grp.sort_values("Position X")
            x = list(grp["Position X"])
            ID_ordenados = (list(grp["ID"]))

            
            # indice = list(grp.index)
            # for pos_ind in range(grp.shape[0]-1):
            #     dist = (x[pos_ind + 1] - x[pos_ind]  )
            #     distancias.append(dist)
            
            distancias = [x[ind]-x[ind-1]  for ind in range(1,len(x),1)]
                      
            vec_i = [None for x in range(grp.shape[0])]
            # vec_d = [""]*grp.shape[0]
            vec_d = [None for x in range(grp.shape[0])]
            di_i = list(grp["Dist_derecha"])
            di_d = list(grp["Dist_izquierda"])
            for pos in range(grp.shape[0]):
                if (pos == 0):
                    closest[pos] = distancias[0]
                    di_d[pos] = distancias[pos]
                    vec_d[pos] = str(ID_ordenados[pos+1])
                    
                else:
                    if (pos > 0 and pos < grp.shape[0]-1):
                        closest[pos]=(min(distancias[pos-1],distancias[pos]))
                        di_i[pos] = distancias[pos-1]
                        di_d[pos] = distancias[pos]
                        vec_i[pos] = str(ID_ordenados[pos-1])
                        vec_d[pos] = str(ID_ordenados[pos+1])
              
                    else:
                        closest[pos]=(distancias[-1])
                        di_i[pos] = distancias[pos-1]
                        vec_i[pos] = str(ID_ordenados[pos-1])
                        
            df.loc[(df["Canal"]==i[0]) & (df["Time"]==i[1]),"Dist_Closest"] = closest
            df.loc[(df["Canal"]==i[0]) & (df["Time"]==i[1]), "Dist_derecha"] = di_d
            df.loc[(df["Canal"]==i[0]) & (df["Time"]==i[1]), "Dist_izquierda"] = di_i
            df.loc[(df["Canal"]==i[0]) & (df["Time"]==i[1]), "Vecino_der"] = vec_d
            df.loc[(df["Canal"]==i[0]) & (df["Time"]==i[1]), "Vecino_izq"] = vec_i       
    return df



def set_agrupada_o_aislada(df, d_cut):
    df["Agrupada"] = False
    df.loc[df["Dist_Closest"]<d_cut,"Agrupada"] = True
    return df



