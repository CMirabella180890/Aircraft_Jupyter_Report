# -*- coding: utf-8 -*-
"""
Created on Sun Nov 14 12:31:36 2021

@author: claum
"""
import pandas
import math
import numpy as np

df = pandas.read_csv('xf-n64212-il-1000000-n5.csv')

Alpha = np.zeros((len(df["Alpha"]), 1))
for i in range(len(df["Alpha"])):
    Alpha[i] = df["Alpha"][i]
    
Cl = np.zeros((len(df["Cl"]), 1))
for i in range(len(df["Cl"])):
    Cl[i] = df["Cl"][i]
    
Cd = np.zeros((len(df["Cd"]), 1))
for i in range(len(df["Cd"])):
    Cd[i] = df["Cd"][i]  
    
Cm = np.zeros((len(df["Cm"]), 1))
for i in range(len(df["Cm"])):
    Cm[i] = df["Cm"][i]     
    
for i in range(len(Alpha)):
    if Alpha[i] == 0: 
        index = i
        
ClAlpha_deg = (Cl[index+1] - Cl[index])/(Alpha[index+1]-Alpha[index])
ClAlpha_rad = ClAlpha_deg*(180.0/math.pi)

AR = 6.40 
CLALPHA_rad = (ClAlpha_rad)/(1 + ((ClAlpha_rad)/(math.pi*AR)))

