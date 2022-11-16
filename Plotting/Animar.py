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
    
    def animate1d(i,df):
        df = df[df["Frame"]==i]
        scatter.set_data(df["Position X"],df["Canal"]) 
        return scatter,
    
    fig, ax = plt.subplots()
    scatter, =  ax.plot([],[],".")
    df["Time"] = [round(t,2) for t in df["Time"]]
    
    radio = 1
    for i in range(max(df["Canal"])+1):
        plt.plot([min(df["Position X"]), max(df["Position X"])] , [i-0.5, i-0.5] , "k-",lw=0.5)
        plt.xlim([min(df["Position X"])-50,max(df["Position X"])+50])
        plt.ylim([-radio , max((df["Canal"]+1)*radio)])
        plt.xlabel(r"Pos X ($\mu$m)")
        plt.ylabel(r"Channel")
    
    n_frames = max(list(df["Frame"]))
    anim = animation.FuncAnimation(fig, animate1d, init_func=init,fargs=[df], frames = range(1,n_frames,1),blit=True)

    return (anim)





def animar_2D(df):
    
    
    def init():
        # initialize an empty list of cirlces
        return []
    
    def animate(i,df):
        
        # l = ax.patches
        while ax.patches:
            ax.patches[0].remove()
            # print(len(ax.patches))
        # for p in ax.patches:
            # p.
        
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