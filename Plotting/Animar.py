#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug  9 17:13:13 2022

@author: lucas
"""



import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from random import randint
from matplotlib import animation

    


def animar_1D(df):
    
    
    def init():
        # initialize an empty list of cirlces
        return []
    
    def animate(i,df):
        
        patches = []
        # ax.patches = []
        for p in ax.patches:
            p.remove()
        
    #    time = i * 0.05
    #    time = round(time,2)
        df = df[df["Frame"]==i]
        for ID, part in df.groupby("ID"):
            patches.append(ax.add_patch( plt.Circle((part["Position X"],2 * part["radio"] * part["Canal"]),part["radio"],fill=False) ))
        
        return patches
    
      
    if not("radio" in df.columns): 
        df["radio"] = 5
    
    fig = plt.figure()
    #plt.axis([min(df["Position X"])-50,max(df["Position X"])+50,-12 , 2*max(df["Canal"])*12])
    ax = plt.gca()
    ax.set_aspect(1)
    df["Time"] = [round(t,2) for t in df["Time"]]
       
    plt.axis([min(df["Position X"])-50,max(df["Position X"])+50,-2*max(df["radio"]) , 2*max(df["Canal"])*max(df["radio"])])
    
    radio = df["radio"][0]
    for i in range(max(df["Canal"])+1):
       plt.plot([min(df["Position X"]), max(df["Position X"])] , [2*i*radio -radio, 2*i*radio - radio] , "k:")
       plt.xlim([min(df["Position X"])-50,max(df["Position X"])+50])
       plt.ylim([-radio , 2*max((df["Canal"]+1)*radio)])
       plt.xlabel(r"Pos X ($\mu$m)")
    
    n_frames = max(list(df["Frame"]))
    anim = animation.FuncAnimation(fig, animate, init_func=init,fargs=[df], frames = range(1,n_frames,1),blit=True)
    return (anim)


def animar_2D(df):
    
    
    def init():
        # initialize an empty list of cirlces
        return []
    
    def animate(i,df):
        for p in ax.patches:
            p.remove()
        
        patches = []
        df = df[df["Frame"]==i]
        for ID, part in df.groupby("ID"):
            patches.append(ax.add_patch( plt.Circle((part["Position X"],part["Position Y"]),part["radio"],fill=False) ))
        
        return patches
    
            
    # data = pd.read_csv("/home/lucas/Escritorio/testeo/1D/6um-rep1_procesado.csv")
    if not("radio" in df.columns): 
        df["radio"] = 5
    
    fig = plt.figure()
    #plt.axis([min(df["Position X"])-50,max(df["Position X"])+50,-12 , 2*max(df["Canal"])*12])
    ax = plt.gca()
    ax.set_aspect(1)
    df["Time"] = [round(t,2) for t in df["Time"]]
       
    plt.axis([min(df["Position X"])-50,max(df["Position X"])+50,-50 , max(df["Position Y"])])
    
    radio = max(list(df["radio"]))
    for c, canal in df.groupby("Canal"):
       plt.plot([min(df["Position X"]), max(df["Position X"])] , [min(canal["Position Y"]) - radio ,min(canal["Position Y"]) - radio ] , "k", lw=0.5)
       plt.plot([min(df["Position X"]), max(df["Position X"])] , [max(canal["Position Y"]) + radio ,max(canal["Position Y"]) + radio ] , "k", lw=0.5)
       # plt.xlim([min(df["Position X"])-50,max(df["Position X"])+50])
     
    plt.ylim([-10 , max(df["Position Y"]) + 10 ])
    plt.xlabel(r"Dim 1 ($\mu$m)")
    plt.ylabel(r"Dim 2 ($\mu$m)")
    
    n_frames = max(list(df["Frame"]))
    anim = animation.FuncAnimation(fig, animate, init_func=init,fargs=[df], frames = range(1,n_frames,1),blit=True)
    return (anim)
    



    
if __name__ == "__main__":
    
    df = pd.read_csv("/home/lucas/Escritorio/testeo/2D/gel/pos3/ pos3_procesado.csv")
    path = "/home/lucas/Escritorio/"
    anim = animar_2D(df)
    anim.save(path+"video1d.gif",dpi=300)