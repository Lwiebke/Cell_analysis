#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 31 12:10:15 2022

@author: lucas
"""

import matplotlib.pyplot as plt
import numpy as np
from scipy.fftpack import fftfreq, ifft
from scipy import signal



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
            


# def autocorr(x,lags):
#     '''fft, pad 0s, non partial'''

#     n=len(x)
#     # pad 0s to 2n-1
#     ext_size=2*n-1
#     # nearest power of 2
#     fsize=2**np.ceil(np.log2(ext_size)).astype('int')

#     xp=x-np.mean(x)
#     var=np.var(x)

#     # do fft and ifft
#     cf=np.fft.fft(xp,fsize)
#     sf=cf.conjugate()*cf
#     corr=np.fft.ifft(sf).real
#     corr=corr/var/n

#     return corr[:len(lags)]


# def plot_vel_autocorrelation(df,path):
#         for j, part in df.groupby("ID"):
#             fig, axs = plt.subplots(2)    
#             print(j)
#             df=df.sort_values("Time")
#             vels = part["Velocidad"]
#             vels = np.asarray(vels)
            
#             lags = np.linspace(0,len(vels),1)

#             autoc = autocorr(vels, lags)
                    
  
#             part.plot(ax=axs[1],x="Time", y='Velocidad', legend=None)
#             axs[1].set_ylabel(r"Velocidad X  ($\mu$m/min)")
            
#             axs[0].plot(lags, autoc, ".")
#             axs[0].set_ylabel(r"Autocorrelacion")
          
            
#             fig.savefig(path+"autocorr_"+str(j)+".png",dpi=200, bbox_inches="tight")
#             plt.close(fig)    
            
            
    
    


#
#def plot_vel_and_fourier(df, path):
#    
#    for j, part in df.groupby("ID"):
#        fig = plt.figure()
#        df=df.sort_values("Time")
#        vels = abs(part["Velocidad"])
#        N = len(vels)
#        n=np.arange(N)
#        fs = 1/20
#        tiempo = n/fs
#        
#
#        f, Pxx_den = signal.periodogram(vels, fs)
#
#        f=1/f
#        f=f/60
#        plt.semilogy(f, Pxx_den)
#    
#        #plt.ylim([1e-7, 1e2])
#    
#        plt.xlabel('Period (min)')
#    
#        plt.ylabel('PSD [V**2/Hz]')
#
#
#        fig.savefig(path+"Periodigram_"+str(j)+".png",dpi=200, bbox_inches="tight")
#        plt.close(fig)    
#        





#
#
#
# def plot_vel_and_fourier(df, path):
    
#     for j, part in df.groupby("ID"):
#         fig, axs = plt.subplots(1)
#         df=df.sort_values("Time")
#         vels = abs(part["Velocidad"])
#         N = len(vels)
#         n=np.arange(N)
#         T = 1/20
        
#         freq = n/T
#         cut_off = 10
#         transform = np.fft.fft(vels)
# #        filtered = transform
# #        filtered[np.abs(freq) < cut_off] = 0
        
        
# #        filtered = ifft(filtered)
# #        part.plot(ax=axs[0],x="Time", y='Velocidad', legend=None)
#         axs.plot(freq, transform)
        
        
#         axs.set_xlabel(r"Frecuencia de velocidad $seg⁻¹ $)",fontsize=16)
     
        

#         fig.savefig(path+"Vel_and_freq_"+str(j)+".png",dpi=200, bbox_inches="tight")
#         plt.close(fig)    
        






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
            


# def plot_pos_n_vel_show_colision(df, path):
    
    
    
#     for canal, df_canal in df.groupby("Canal"):
#         fig, axs = plt.subplots(2)
#         for j, part in df_canal.groupby("ID"):
#             if any(part["Colision"]):    
#                 #fig, axs = plt.subplots(2)       
#                 part.plot(ax=axs[0],x="Time", y='Position X',marker=".", label=j)
#                 part.plot(ax=axs[1],x="Time", y='Velocidad',marker=".", legend=None)
#                 axs[1].plot(part[part["Colision"]]["Time"],part[part["Colision"]]["Velocidad"],"rX")
#                 axs[0].plot(part[part["Colision"]]["Time"],part[part["Colision"]]["Position X"],"rX")
#                 axs[0].set_ylabel(r"Posicion X: $\mu$m")
#                 axs[1].set_ylabel(r"Velocidad X  ($\mu$m/min)")
#                 axs[1].plot([0,70],[0,0],"r:")
#                 axs[1].plot(part[part["Collision_solved"]]["Time"],part[part["Collision_solved"]]["Position X"],"gx")
                
#         fig.savefig(path+"Colision_"+str(canal)+".png",dpi=200, bbox_inches="tight")
#         plt.close(fig)    
                





#from matplotlib.ticker import (AutoMinorLocator, MultipleLocator)

def plot_pos_by_channel(df, path,show_colision=False):
        
    for canal, df_canal in df.groupby("Canal"):
        fig, axs = plt.subplots(1)
        for j, part in df_canal.groupby("ID"):
            
            part.plot(ax=axs,x="Time", y = 'Position X', lw = 0.5, label = j)

            
            axs.set_ylabel(r"Position X: $\mu$m")
            axs.set_xlabel(r"Time (min)")
            axs.grid()
         
            if show_colision:
                axs.plot(part[part["Colision"]]["Time"],part[part["Colision"]]["Position X"],"rx")
                axs.plot(part[part["Collision_solved"]]["Time"],part[part["Collision_solved"]]["Position X"],"gx")
            # plt.legend()
        fig.savefig(path+"canal_"+str(canal)+".png",dpi=500, bbox_inches="tight")
        plt.close(fig)
        
            