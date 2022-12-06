#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec  1 11:38:20 2022

@author: lucas
"""


import pandas as pd
import numpy as np
from scipy.spatial.distance import cdist
from scipy.optimize import linear_sum_assignment



def track_cells(df,unasigned_track,unasigned_det_cost):

    df=df.sort_values("Frame")
    for c, df_canal in df.groupby("Canal"):
        frames = list(set(df_canal["Frame"]))
        
        for f in frames[:-1]:
            tracks = df_canal.loc[df_canal["Frame"]==f,["ID","Position X","Position Y"]]
            detections = df_canal.loc[df_canal["Frame"]==f+1,["ID","Position X","Position Y"]]
            
            tracks = tracks.reset_index(drop=True)
            detections = detections.reset_index(drop=True)
            
            n_tracks = len(tracks)
            n_det = len(detections)
                        
            cost = cdist(np.asarray(tracks.loc[:,["Position X","Position Y"]]),np.asarray(detections.loc[:,["Position X","Position Y"]]))
            
            """ Fill with unasigned cost """
            # To give every track and det the posibility of being unassigned
            
            added_columns = unasigned_track * np.ones([n_tracks,n_tracks]) 
            added_rows = unasigned_det_cost *np.ones([n_det,n_det+n_tracks])
            added_rows[ : , n_det: ] = float(0)
            
            cost = np.append(cost, added_columns,axis = 1)
            cost = np.append(cost, added_rows, axis = 0)
            
            row, col = linear_sum_assignment(cost)
            col=col[0:n_tracks]
                        
            """ Use the assignments to name the IDs """
            for i,pos in enumerate(col):
                if pos < n_det:

                    df.loc[ df["ID"] == detections.loc[pos,"ID"] , "ID"] = tracks.loc[i,"ID"]
                    df_canal.loc[ df_canal["ID"] == detections.loc[pos,"ID"] , "ID"] = tracks.loc[i,"ID"]
                 
    return df





def track_cells_memory(df,cost,memory_frames,borders_width=50):
    
    unasigned_track=cost
    unasigned_det_cost=cost
    max_x = max(df["Position X"])
    df=df.sort_values("Frame")

    for c, df_canal in df.groupby("Canal"):
        frames = list(set(df_canal["Frame"]))
        wait_list = [ ]
        for f in frames[:-1]:
           
            for i in range(len(wait_list)):
                wait_list[i][1] -= 1
            wait_list = [x for x in wait_list if x[1] > 0]
          
            tracks = df_canal.loc[df_canal["Frame"]==f,["ID","Position X","Position Y"]]
            detections = df_canal.loc[df_canal["Frame"]==f+1,["ID","Position X","Position Y"]]
            
            tracks = tracks.reset_index(drop=True)
            detections = detections.reset_index(drop=True)
            
            n_tracks = len(tracks)
            n_det = len(detections)
                        
            cost = cdist(np.asarray(tracks.loc[:,["Position X","Position Y"]]),np.asarray(detections.loc[:,["Position X","Position Y"]]))
            
            """ Fill with unasigned cost """
            # To give every track and det the posibility of being unassigned
            
            added_columns = unasigned_track * np.ones([n_tracks,n_tracks]) 
            added_rows = unasigned_det_cost *np.ones([n_det,n_det+n_tracks])
            added_rows[ : , n_det: ] = float(0)
            
            cost = np.append(cost, added_columns,axis = 1)
            cost = np.append(cost, added_rows, axis = 0)
            
            row, col = linear_sum_assignment(cost)
    
    
            """ Use the assignments to name the IDs """
            for i,pos in enumerate(col): 
                
                
                if i < n_tracks: #para las deteciones, asigno el track encontrado (si hay)
                    if pos < n_det:
                        df.loc[ df["ID"] == detections.loc[pos,"ID"] , "ID"] = tracks.loc[i,"ID"]
                        df_canal.loc[ df_canal["ID"] == detections.loc[pos,"ID"] , "ID"] = tracks.loc[i,"ID"]
                        
                    else: # si no hay un deteccion que corresponda y no estaba cerca de los bordes, queda en espera
                        if (tracks.loc[i,"Position X"] < (max_x - borders_width)) and (tracks.loc[i,"Position X"] > borders_width): 
                            wait_list.append( [tracks.loc[i,"ID"],memory_frames,tracks.loc[i,"Position X"]]  )
                        
                    
                              
                if (i >= n_tracks) and  (pos < n_det): #cuando encuentro una que no pude asignar a ninguna del frame anterior...
                     
                    if (  (detections.loc[pos,"Position X"] < (max_x - borders_width)) and (detections.loc[pos,"Position X"] > borders_width)  ):
                        if len(wait_list)>0:
                             distancias = []
                             for candidato in wait_list: # Busco entre las que están en espera para ver si coincide
                                 distancias.append(abs(detections.loc[pos,"Position X"] - candidato[2] ))
                             if min(distancias) < unasigned_det_cost:
                                
                                pos_elegido = distancias.index(min(distancias)) 
                                ID_elegido = wait_list.pop(pos_elegido)[0]
                                df.loc[ df["ID"] == detections.loc[pos,"ID"] , "ID"] = ID_elegido
                                df_canal.loc[ df_canal["ID"] == detections.loc[pos,"ID"] , "ID"] = ID_elegido
                                # print(str(detections.loc[pos,"ID"])+" se encontró pero no tiene track, se le asignó: " + str(ID_elegido) + " porque había desaparecido")
                        else: # Si no está cerca de los bordes, y no se vio antes, se elimina (posible error de segmentación)
                            print(str(detections.loc[pos,"ID"]) +" salió de la nada en el frame "+str(f) +" y canal " + str(c) )
                            df.drop(df.index[df["ID"] == detections.loc[pos,"ID"]],axis=0,inplace=True)
                            df_canal.drop(df_canal.index[df_canal["ID"] == detections.loc[pos,"ID"]],axis=0,inplace=True)
     
        
    
    return df
   




# if __name__ == "__main__":
    

