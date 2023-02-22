#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 28 12:14:48 2022

@author: lucas
"""



import pandas as pd
import jenkspy
import matplotlib.pyplot as plt
import numpy as np


def asignar_canales( df, num_canales, pendiente):

    """  Usando natural breaks de jenkins, separo las posiciones en Y en grupos, 
cada grupo representa a un canal, dado que los canales son constantes en y 
y tienen una distancia entre ellos mayor al ancho del canal, es una separación 
razonable. """
    


    medio = max(df["Position X"])-min(df["Position X"])/2.0
    df['Position Y aux'] = df['Position Y'] + pendiente*(df["Position X"]-medio)

    breaks = jenkspy.jenks_breaks(df['Position Y aux'], n_classes=num_canales)
    df['Canal'] = pd.cut(df['Position Y aux'],
                        bins=breaks,
                        labels=range(num_canales),
                        include_lowest=True)
    
    df["Canal"] = df["Canal"].astype("category")
       
    return df


def asignar_canales_dbscan(df,eps,min_samples):
    from sklearn.neighbors import NearestNeighbors
    
    from sklearn.cluster import DBSCAN

    
    X = np.asarray(df.loc[:,["Position X","Position Y"]])
    
    
    neigh = NearestNeighbors(n_neighbors=2)
    nbrs = neigh.fit(X)
    distances, indices = nbrs.kneighbors(X)
    
    distances=np.sort(distances,axis=0)
    distances = distances[:,1]
    
  
    clustering = DBSCAN(eps=eps,min_samples=min_samples).fit(X)
  
    df["Canal"] = clustering.labels_   
    df["Canal"] = df["Canal"].astype("category")
        
    return df
  
    
def asignar_canales_kmeans(df,k):
    from sklearn.cluster import KMeans
    
    sub_df=df.loc[:,["Position X","Position Y"]]
    kmeans = KMeans(n_clusters=k).fit(sub_df)
        
    df.loc[:,"Canal"]=kmeans.labels_
    
    return df
    
  
    
  
    
  
    
  
    
  
    
  
    
      
def plot_channels(df):
    from random import randint
    
    fig = plt.figure()
    color={}
    for i in list(set(list(df['Canal']))):
        color[i]=('#%06X' % randint(0, 0xFFFFFF))
    plt.scatter(df["Position X"], df["Position Y"],c=df["Canal"].map(color),s=3)
       
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
