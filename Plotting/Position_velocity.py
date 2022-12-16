#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 31 12:10:15 2022

@author: lucas
"""

import matplotlib.pyplot as plt

def plot_pos_n_vel(df, path, show_colision=False):
    
    for j, part in df.groupby("ID"):
        # if any(part["Colision"]):    
            fig, axs = plt.subplots(2)       
            part.plot(ax=axs[0],x="Time", y='Position X', label=j)
            part.plot(ax=axs[1],x="Time", y='Velocidad', legend=None)
            
            
            axs[0].set_xlabel(" ")
            axs[1].set_xlabel("Time (min)")
            
            axs[0].set_ylabel(r"Position X: $\mu$m")
            axs[1].set_ylabel(r"Velocity X  ($\mu$m/min)")
            
            if show_colision:          
                axs[1].plot(part[part["Colision"]]["Time"],part[part["Colision"]]["Velocidad"],"rX")
                axs[1].plot(part[part["Collision_solved"]]["Time"],part[part["Collision_solved"]]["Velocidad"],"gx")
                axs[0].plot(part[part["Colision"]]["Time"],part[part["Colision"]]["Position X"],"rX")
                axs[0].plot(part[part["Collision_solved"]]["Time"],part[part["Collision_solved"]]["Position X"],"gx")
                
            axs[1].plot([min(list(part["Time"])),max(list(part["Time"]))],[0,0],"r:")
            
            fig.tight_layout()
            
            fig.savefig(path+"cell_"+str(j)+".png",dpi=300, bbox_inches="tight")
            plt.close(fig)    
            

         

def plot_pos_by_channel(df, path,show_colision=False):
        
    for canal, df_canal in df.groupby("Canal"):
        fig, axs = plt.subplots(1)
        for j, part in df_canal.groupby("ID"):
            
            part.plot(ax=axs,x="Time", y = 'Position X', lw = 0.5,label=j)

            
            axs.set_ylabel(r"Position X: $\mu$m")
            axs.set_xlabel(r"Time (min)")
            axs.grid()
         
            if show_colision:
                axs.plot(part[part["Colision"]]["Time"],part[part["Colision"]]["Position X"],"rx")
                axs.plot(part[part["Collision_solved"]]["Time"],part[part["Collision_solved"]]["Position X"],"gx")
            plt.legend()
        fig.savefig(path+"canal_"+str(canal)+".png",dpi=500, bbox_inches="tight")
        plt.close(fig)
        
 
    






# def plot_pos_n_vel_show_inversion(df, path):
    
#     for j, part in df.groupby("ID"):
# #        if any(part["Inversion"]):    
#             fig, axs = plt.subplots()       
# #            part.plot(ax=axs[0],x="Time", y='Position X',marker=".", label=j)
#             part.plot(ax=axs,x="Time", y='Velocidad',marker=".", legend=None)
# #            axs.plot(part[part["Inversion"]]["Time"],part[part["Inversion"]]["Velocidad"],"r*")
#             axs.set_xlabel("Tiempo (min)",fontsize=14)
# #            axs[0].plot(part[part["Inversion"]]["Time"],part[part["Inversion"]]["Position X"],"r*")
# #            axs[0].set_ylabel(r"Posicion X: $\mu$m")
#             axs.set_ylabel(r"Velocidad ($\mu$m/min)",fontsize=14)
#             axs.plot([min(list(part["Time"])),max(list(part["Time"]))],[0,0],"r:")
#             axs.grid()
#             fig.savefig(path+"Flip_media_in_cell_"+str(j)+".png",dpi=200, bbox_inches="tight")
#             plt.close(fig)    
            

        
        
        
            