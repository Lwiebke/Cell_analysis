#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 12 17:13:33 2022

@author: lucas
"""


import pandas as pd

def definir_trenes(df, d_cut):
     
    
    """ Trains are defined as cells that are closer than a given distance.   """
    
    
    df["Tren_ID"] = df["ID"] ##al iniciar, cada celulas es su propio tren
    df.sort_values("Position X")
    for i, grp in df.groupby(["Canal","Time"]):
        if grp.shape[0] > 1:

            grp = grp.sort_values("Position X")
            x = list(grp["Position X"])
            IDs = list(grp["ID"])

            for j in range(len(x)-1):
                dist =  x[j+1] - x[j]  
                if (dist < d_cut):
                    
                    grp.loc[grp["ID"]==IDs[j+1],"Tren_ID"] = str(grp.loc[grp["ID"]==IDs[j],"Tren_ID"].item())

            
            df.loc[(df["Canal"] == i[0]) & (df["Time"] == i[1]),"Tren_ID"] = grp["Tren_ID"]

    return df

