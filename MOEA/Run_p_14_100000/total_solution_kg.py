# -*- coding: utf-8 -*-
"""
Created on Wed May 25 10:39:48 2022

@author: eari
"""

import pandas as pd
import numpy as np

version = 'district'

#####################################################################
##########           IMPORT DATA           ##########################
#####################################################################

# import excel sheet  
df_geo_corn = pd.read_excel('combined_pivot_corn_excel_electricity.xlsx',header=0, engine='openpyxl') #contains data sets for corn (state, land cost, yield etc)
df_geo_soy = pd.read_excel('combined_pivot_soy_excel_electricity.xlsx',header=0, engine='openpyxl') #contains data sets for soy (state, land cost, yield etc)
df_geo_grass = pd.read_excel('combined_pivot_grass_excel_electricity.xlsx',header=0, engine='openpyxl') #contains data sets for grass (state, land cost, yield etc) 
df_geo_algae = pd.read_excel('combined_pivot_algae_excel_electricity.xlsx',header=0, engine='openpyxl') #contains data sets for algae (state, land cost, yield etc) 

districts = list(df_geo_corn['STASD_N']) # list of ag_district code

df_ha =  pd.read_csv('Decision_Variables_borg_two_crop_trialdistrict.csv',header=0) #contains data sets for used hectare

C_ha = np.transpose(df_ha).iloc[1:108].values # used hectare for corn 
S_ha = np.transpose(df_ha).iloc[1:108].values # used hectare for soy
G_ha = np.transpose(df_ha).iloc[108:215].values # used hectare for grass
A_ha = np.transpose(df_ha).iloc[215:].values # used hectare for algae

LC = df_geo_corn.loc[:,'land_costs-$/ha'].values # $ per ha

years = range(1998,2014)
solution = range(len(df_ha))


# Corn Grain yield
C_yield = df_geo_corn.loc[:,1998:2013].values  #yield in kg/ha

# Soybean yield
S_yield = df_geo_soy.loc[:,1998:2013].values  #yield in kg/ha

# Grass yield
G_yield = df_geo_grass.loc[:,1998:2013].values  #yield in kg/ha

# Algae yield
A_yield = df_geo_algae.loc[:,1998:2013].values  #yield in kg/ha

num_c = np.size(LC) #size of land cost 
Energy_total = np.zeros((len(years),1))


CG_kg_tot = np.zeros((1,len(df_ha)))
SB_kg_tot = np.zeros((1,len(df_ha)))
G_kg_tot = np.zeros((1,len(df_ha)))
A_kg_tot = np.zeros((1,len(df_ha)))

Y = C_yield[:,15]   # corn yield kg/ha
S = S_yield[:,15]   # soy yield kg/ha
G = G_yield[:,15]   # grass yield kg/ha
A = A_yield[:,15]   # algae yield kg/ha

for s in solution:
    CG_prod = sum(C_ha[:,s]*Y) 
    CG_kg_tot[:,s] = CG_prod         # total corn biomass production (kg)
        
    SB_prod = sum(S_ha[:,s]*S)
    SB_kg_tot[:,s] = SB_prod         # total soy biomass production (kg)
        
        
    G_prod = sum(G_ha[:,s]*G)
    G_kg_tot[:,s] = G_prod           # total grass biomass production (kg)
        
    A_prod = sum(A_ha[:,s]*A)
    A_kg_tot[:,s] = A_prod           # total algae biomass production (kg)

CG_total = np.transpose(CG_kg_tot)
SB_total = np.transpose(SB_kg_tot)
G_total = np.transpose(G_kg_tot)
A_total = np.transpose(A_kg_tot)

Total = CG_total + SB_total + G_total + A_total