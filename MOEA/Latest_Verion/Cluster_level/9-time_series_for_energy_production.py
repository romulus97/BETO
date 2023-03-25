# -*- coding: utf-8 -*-
"""
Created on Wed Jan 11 18:03:56 2023

@author: eari
"""

# library
import numpy as np
import matplotlib.pyplot as plt

import pandas as pd
import plotly.io as pio
pio.renderers.default='browser'
import plotly.express as px
import matplotlib.patches as mpatches


# import excel sheet  
df_geo_corn = pd.read_excel('Platypus_codes/combined_pivot_Corn.xlsx',header=0, engine='openpyxl') #contains data sets for corn (state, land cost, yield etc)
df_geo_soy = pd.read_excel('Platypus_codes/combined_pivot_Soy.xlsx',header=0, engine='openpyxl') #contains data sets for soy (state, land cost, yield etc)
df_geo_grass_L = pd.read_excel('Platypus_codes/combined_pivot_AG_Switchgrass.xlsx',header=0, engine='openpyxl') #contains data sets for grass (state, land cost, yield etc) 
df_geo_grass = pd.read_excel('Platypus_codes/combined_pivot_ML_Switchgrass.xlsx',header=0, engine='openpyxl') #contains data sets for grass (state, land cost, yield etc) 
df_geo_algae_L = pd.read_excel('Platypus_codes/combined_pivot_AG_Algae.xlsx',header=0, engine='openpyxl') #contains data sets for algae (state, land cost, yield etc)   
df_geo_algea = pd.read_excel('Platypus_codes/combined_pivot_ML_Algae.xlsx',header=0, engine='openpyxl') #contains data sets for algae (state, land cost, yield etc) 

districts = list(df_geo_corn['STASD_N']) # list of ag_district code
num_c = len(df_geo_corn)

years = range(1998,2014)

# Corn Grain yield
C_yield = df_geo_corn.loc[:,1998:2013].values  #yield in kg/ha

# Soybean yield
S_yield = df_geo_soy.loc[:,1998:2013].values  #yield in kg/ha

# Grass yield
G_yield_L = df_geo_grass_L.loc[:,1998:2013].values  #yield in kg/ha

G_yield = df_geo_grass.loc[:,1998:2013].values  #yield in kg/ha

# Algea yield
A_yield_L = df_geo_algae_L.loc[:,1998:2013].values  #yield in kg/ha

A_yield = df_geo_algea.loc[:,1998:2013].values  #yield in kg/ha


# objective = 'min_GHG_emission'

fig = plt.figure(figsize=(10,5))

# version = ['district','_0.001district','_100000_0.1district','_100000_0.001district',
#             '_1000000_0.1district','_1000000_0.001district','_10000000_0.1district','_10000000_0.001district']


# version = ['_100000_0.1district']
# version = ['_100000_0.001district']
# version = ['_1000000_0.1district']
# version = ['_1000000_0.001district']
# version = ['_10000000_0.1district']
version = ['_10000000_0.001district']


for v in version:
    
    # objective = 'max_energy_shortfall'
    # # objective = 'cost'

    # ## 3 billion ###
    
    # fn_ha3 = 'Decision_Variables_borg_crops_GHG3' + v + '_PARETO'  +'.csv'
    # df_ha3 = pd.read_csv(fn_ha3, header=0, index_col=0)
    
    # fn3 = 'Objective_functions_borg_crops_GHG3' + v + '_PARETO'  +'.csv'
    # df_O3 = pd.read_csv(fn3, header=0, index_col=0)
    
    # df_O3.columns = ['cost','max_energy_shortfall','min_GHG_emission']
    # sorting3 = df_O3.sort_values(by= objective, ascending=True).head(1)
    
    
    # my_index3 = list(sorting3.index)
    # df_ha3_sorted = df_ha3.loc[my_index3]
    
    # C_ha_AG3 = (np.transpose(df_ha3_sorted).iloc[0:num_c].values)/2 # used hectare for corn 
    # S_ha_AG3 = (np.transpose(df_ha3_sorted).iloc[0:num_c].values)/2 # used hectare for soy
    # G_ha_ML3 = (np.transpose(df_ha3_sorted).iloc[num_c:2*num_c].values) # used hectare for grass
    # A_ha_ML3 = (np.transpose(df_ha3_sorted).iloc[2*num_c:3*num_c].values) # used hectare for algae
    # G_ha_AG3 = (np.transpose(df_ha3_sorted).iloc[3*num_c:4*num_c].values) # used hectare for grass
    # A_ha_AG3 = (np.transpose(df_ha3_sorted).iloc[4*num_c:].values) # used hectare for algae
    
    
    # Corn_energy_yearly3 = np.zeros((len(years)))
    # Soy_energy_yearly3 = np.zeros((len(years)))
    # Grass_energy_yearly3 = np.zeros((len(years)))
    # Algae_energy_yearly3 = np.zeros((len(years)))
    # Grass_AG_energy_yearly3 = np.zeros((len(years)))
    # Algae_AG_energy_yearly3 = np.zeros((len(years)))
    # Total_energy3 = np.zeros((len(years)))
    # Total_p3 = np.zeros((len(years)))
    # Percentage3 = np.zeros((len(years)))
    
    # for year in years:
    #     i = years.index(year)
    #     Y3 = C_yield[:,i]  # corn yield kg/ha
    #     S3 = S_yield[:,i]   # soy yield kg/ha
    #     G3 = G_yield[:,i]   # grass yield kg/ha
    #     A3 = A_yield[:,i]   # algae yield kg/ha
    #     G_L3 = G_yield_L[:,i]   # grass yield kg/ha
    #     A_L3 = A_yield_L[:,i]   # algae yield kg/ha
        
    #     Corn_kg3 = C_ha_AG3.reshape(-1)*Y3.reshape(-1)
    #     Corn_ethanol_con3 = sum(Corn_kg3*9.42)   #MJ/kg
    #     Corn_energy_yearly3[i] =Corn_ethanol_con3
        
    #     Soy_kg3 = S_ha_AG3.reshape(-1)*S3.reshape(-1) 
    #     Soy_Oil_con3 = sum(Soy_kg3*8.02)   #MJ/kg
    #     Soy_energy_yearly3[i] =Soy_Oil_con3
        
    #     Grass_kg3 = G_ha_ML3.reshape(-1)*G3.reshape(-1)
    #     Biocrude_con3 = sum(Grass_kg3*8.35)   #MJ/kg
    #     Grass_energy_yearly3[i] =Biocrude_con3
        
    #     Algae_kg3 = A_ha_ML3.reshape(-1)*A3.reshape(-1)
    #     Algal_Oil_con3 = sum(Algae_kg3*20.82)   #MJ/kg
    #     Algae_energy_yearly3[i] =Algal_Oil_con3
        
    #     Grass_AG_kg3 = G_ha_AG3.reshape(-1)*G_L3.reshape(-1)
    #     Biocrude_con_AG3 = sum(Grass_AG_kg3*8.35)   #MJ/kg
    #     Grass_AG_energy_yearly3[i] =Biocrude_con_AG3
        
    #     Algae_AG_kg3 = A_ha_AG3.reshape(-1)*A_L3.reshape(-1)
    #     Algal_Oil_con_AG3 = sum(Algae_AG_kg3*20.82)   #MJ/kg
    #     Algae_AG_energy_yearly3[i] =Algal_Oil_con_AG3
        
    #     Total3 = Corn_ethanol_con3 + Soy_Oil_con3 + Biocrude_con3 + Algal_Oil_con3 + Biocrude_con_AG3 + Algal_Oil_con_AG3
    #     bg3 = 3 ## We will try 0, 3, 6, 9, 12, 15, 18, 20
    #     bgg3 =  bg3*10**9
    #     con3 = 30.81*(1/0.2641)  ## MJ/litre * liter/gallons
    #     quota3 = bgg3*con3  ## energy as MJ/yr
    #     Total_p3[i] = Total3
    #     Total_energy3[i] = Total3 - quota3
    #     Percentage3[i] = Total_energy3[i]*100/quota3
    
    # plt.plot(range(1998,2014),Percentage3, label="3 billion")
    
    # ### 6 billion ###
    
    # fn_ha6 = 'Decision_Variables_borg_crops_GHG6' + v + '_PARETO'  +'.csv'
    # df_ha6 = pd.read_csv(fn_ha6,header=0,index_col=0)
    
    # fn6 = 'Objective_functions_borg_crops_GHG6' + v + '_PARETO'  +'.csv'
    # df_O6 = pd.read_csv(fn6,header=0,index_col=0)
    
    # df_O6.columns = ['cost','max_energy_shortfall','min_GHG_emission']
    # sorting6 = df_O6.sort_values(by= objective, ascending=True).head(1)
    
    
    # my_index6 = list(sorting6.index)
    # df_ha6_sorted = df_ha6.loc[my_index6]
    
    # C_ha_AG6 = (np.transpose(df_ha6_sorted).iloc[0:num_c].values)/2 # used hectare for corn 
    # S_ha_AG6 = (np.transpose(df_ha6_sorted).iloc[0:num_c].values)/2 # used hectare for soy
    # G_ha_ML6 = (np.transpose(df_ha6_sorted).iloc[num_c:2*num_c].values) # used hectare for grass
    # A_ha_ML6 = (np.transpose(df_ha6_sorted).iloc[2*num_c:3*num_c].values) # used hectare for algae
    # G_ha_AG6 = (np.transpose(df_ha6_sorted).iloc[3*num_c:4*num_c].values) # used hectare for grass
    # A_ha_AG6 = (np.transpose(df_ha6_sorted).iloc[4*num_c:].values) # used hectare for algae
    
    # Corn_energy_yearly6 = np.zeros((len(years)))
    # Soy_energy_yearly6 = np.zeros((len(years)))
    # Grass_energy_yearly6 = np.zeros((len(years)))
    # Algae_energy_yearly6 = np.zeros((len(years)))
    # Grass_AG_energy_yearly6 = np.zeros((len(years)))
    # Algae_AG_energy_yearly6 = np.zeros((len(years)))
    # Total_energy6 = np.zeros((len(years)))
    # Percentage6 = np.zeros((len(years)))
    
    # for year in years:
    #     i = years.index(year)
    #     Y6 = C_yield[:,i]   # corn yield kg/ha
    #     S6 = S_yield[:,i]   # soy yield kg/ha
    #     G6 = G_yield[:,i]   # grass yield kg/ha
    #     A6 = A_yield[:,i]   # algae yield kg/ha
    #     G_L6 = G_yield_L[:,i]   # grass yield kg/ha
    #     A_L6 = A_yield_L[:,i]   # algae yield kg/ha
        
    #     Corn_kg6 = C_ha_AG6.reshape(-1)*Y6.reshape(-1) 
    #     Corn_ethanol_con6 = sum(Corn_kg6*9.42)   #MJ/kg
    #     Corn_energy_yearly6[i] =Corn_ethanol_con6
        
    #     Soy_kg6 = S_ha_AG6.reshape(-1)*S6.reshape(-1)
    #     Soy_Oil_con6 = sum(Soy_kg6*8.02)   #MJ/kg
    #     Soy_energy_yearly6[i] =Soy_Oil_con6
        
    #     Grass_kg6 = G_ha_ML6.reshape(-1)*G6.reshape(-1)
    #     Biocrude_con6 = sum(Grass_kg6*8.35)   #MJ/kg
    #     Grass_energy_yearly6[i] =Biocrude_con6
        
    #     Algae_kg6 = A_ha_ML6.reshape(-1)*A6.reshape(-1)
    #     Algal_Oil_con6 = sum(Algae_kg6*20.82)   #MJ/kg
    #     Algae_energy_yearly6[i] =Algal_Oil_con6
        
    #     Grass_AG_kg6 = G_ha_AG6.reshape(-1)*G_L6.reshape(-1)
    #     Biocrude_con_AG6 = sum(Grass_AG_kg6*8.35)   #MJ/kg
    #     Grass_AG_energy_yearly6[i] =Biocrude_con_AG6
        
    #     Algae_AG_kg6 = A_ha_AG6.reshape(-1)*A_L6.reshape(-1)
    #     Algal_Oil_con_AG6 = sum(Algae_AG_kg6*20.82)   #MJ/kg
    #     Algae_AG_energy_yearly6[i] =Algal_Oil_con_AG6
        
    #     Total6 = Corn_ethanol_con6 + Soy_Oil_con6 + Biocrude_con6 + Algal_Oil_con6 + Biocrude_con_AG6 + Algal_Oil_con_AG6
    #     bg6 = 6 ## We will try 0, 3, 6, 9, 12, 15, 18, 20
    #     bgg6 =  bg6*10**9
    #     con6 = 30.81*(1/0.2641)  ## MJ/litre * liter/gallons
    #     quota6 = bgg6*con6  ## energy as MJ/yr
    #     Total_energy6[i] = Total6 - quota6
    #     Percentage6[i] = Total_energy6[i]*100/quota6
        
    # plt.plot(range(1998,2014),Percentage6, label="6 billion")
    
    # ### 9 billion ###
    
    # fn_ha9 = 'Decision_Variables_borg_crops_GHG9' + v + '_PARETO'  +'.csv'
    # df_ha9 = pd.read_csv(fn_ha9,header=0,index_col=0)
    
    # fn9 = 'Objective_functions_borg_crops_GHG9' + v + '_PARETO'  +'.csv'
    # df_O9 = pd.read_csv(fn9,header=0,index_col=0)
    
    # df_O9.columns = ['cost','max_energy_shortfall','min_GHG_emission']
    # sorting9 = df_O9.sort_values(by= objective, ascending=True).head(1)
    
    
    # my_index9 = list(sorting9.index)
    # df_ha9_sorted = df_ha9.loc[my_index9]
    
    
    # C_ha_AG9 = (np.transpose(df_ha9_sorted).iloc[0:num_c].values)/2 # used hectare for corn 
    # S_ha_AG9 = (np.transpose(df_ha9_sorted).iloc[0:num_c].values)/2 # used hectare for soy
    # G_ha_ML9 = (np.transpose(df_ha9_sorted).iloc[num_c:2*num_c].values) # used hectare for grass
    # A_ha_ML9 = (np.transpose(df_ha9_sorted).iloc[2*num_c:3*num_c].values) # used hectare for algae
    # G_ha_AG9 = (np.transpose(df_ha9_sorted).iloc[3*num_c:4*num_c].values) # used hectare for grass
    # A_ha_AG9 = (np.transpose(df_ha9_sorted).iloc[4*num_c:].values) # used hectare for algae
    
    # Corn_energy_yearly9 = np.zeros((len(years)))
    # Soy_energy_yearly9 = np.zeros((len(years)))
    # Grass_energy_yearly9 = np.zeros((len(years)))
    # Algae_energy_yearly9 = np.zeros((len(years)))
    # Grass_AG_energy_yearly9 = np.zeros((len(years)))
    # Algae_AG_energy_yearly9 = np.zeros((len(years)))
    # Total_energy9 = np.zeros((len(years)))
    # Percentage9 = np.zeros((len(years)))
    
    # for year in years:
    #     i = years.index(year)
    #     Y9 = C_yield[:,i]   # corn yield kg/ha
    #     S9 = S_yield[:,i]   # soy yield kg/ha
    #     G9 = G_yield[:,i]   # grass yield kg/ha
    #     A9 = A_yield[:,i]   # algae yield kg/ha
    #     G_L9 = G_yield_L[:,i]   # grass yield kg/ha
    #     A_L9 = A_yield_L[:,i]   # algae yield kg/ha
        
    #     Corn_kg9 = C_ha_AG9.reshape(-1)*Y9.reshape(-1) 
    #     Corn_ethanol_con9 = sum(Corn_kg9*9.42)   #MJ/kg
    #     Corn_energy_yearly9[i] =Corn_ethanol_con9
        
    #     Soy_kg9 = S_ha_AG9.reshape(-1)*S9.reshape(-1)
    #     Soy_Oil_con9 = sum(Soy_kg9*8.02)   #MJ/kg
    #     Soy_energy_yearly9[i] =Soy_Oil_con9
        
    #     Grass_kg9 = G_ha_ML9.reshape(-1)*G9.reshape(-1)
    #     Biocrude_con9 = sum(Grass_kg9*8.35)   #MJ/kg
    #     Grass_energy_yearly9[i] =Biocrude_con9
        
    #     Algae_kg9 = A_ha_ML9.reshape(-1)*A9.reshape(-1)
    #     Algal_Oil_con9 = sum(Algae_kg9*20.82)   #MJ/kg
    #     Algae_energy_yearly9[i] =Algal_Oil_con9
        
    #     Grass_AG_kg9 = G_ha_AG9.reshape(-1)*G_L9.reshape(-1)
    #     Biocrude_con_AG9 = sum(Grass_AG_kg9*8.35)   #MJ/kg
    #     Grass_AG_energy_yearly9[i] =Biocrude_con_AG9
        
    #     Algae_AG_kg9 = A_ha_AG9.reshape(-1)*A_L9.reshape(-1)
    #     Algal_Oil_con_AG9 = sum(Algae_AG_kg9*20.82)   #MJ/kg
    #     Algae_AG_energy_yearly9[i] =Algal_Oil_con_AG9
        
    #     Total9 = Corn_ethanol_con9 + Soy_Oil_con9 + Biocrude_con9 + Algal_Oil_con9 + Biocrude_con_AG9 + Algal_Oil_con_AG9
    #     bg9 = 9 ## We will try 0, 3, 6, 9, 12, 15, 18, 20
    #     bgg9 =  bg9*10**9
    #     con9 = 30.81*(1/0.2641)  ## MJ/litre * liter/gallons
    #     quota9 = bgg9*con9  ## energy as MJ/yr
    #     Total_energy9[i] = Total9 - quota9
    #     Percentage9[i] = Total_energy9[i]*100/quota9
    
    # plt.plot(range(1998,2014),Percentage9, label="9 billion")
    
    # ### 12 billion ###
    
    # fn_ha12 = 'Decision_Variables_borg_crops_GHG12' + v + '_PARETO'  +'.csv'
    # df_ha12 = pd.read_csv(fn_ha12,header=0,index_col=0)
    
    # fn12 = 'Objective_functions_borg_crops_GHG12' + v + '_PARETO'  +'.csv'
    # df_O12 = pd.read_csv(fn12,header=0,index_col=0)
    
    # df_O12.columns = ['cost','max_energy_shortfall','min_GHG_emission']
    # sorting12 = df_O12.sort_values(by= objective, ascending=True).head(1)
    
    # my_index12 = list(sorting12.index)
    # df_ha12_sorted = df_ha12.loc[my_index12]
    
    
    # C_ha_AG12 = (np.transpose(df_ha12_sorted).iloc[0:num_c].values)/2 # used hectare for corn 
    # S_ha_AG12 = (np.transpose(df_ha12_sorted).iloc[0:num_c].values)/2 # used hectare for soy
    # G_ha_ML12 = (np.transpose(df_ha12_sorted).iloc[num_c:2*num_c].values) # used hectare for grass
    # A_ha_ML12 = (np.transpose(df_ha12_sorted).iloc[2*num_c:3*num_c].values) # used hectare for algae
    # G_ha_AG12 = (np.transpose(df_ha12_sorted).iloc[3*num_c:4*num_c].values) # used hectare for grass
    # A_ha_AG12 = (np.transpose(df_ha12_sorted).iloc[4*num_c:].values) # used hectare for algae
    
    # Corn_energy_yearly12 = np.zeros((len(years)))
    # Soy_energy_yearly12 = np.zeros((len(years)))
    # Grass_energy_yearly12 = np.zeros((len(years)))
    # Algae_energy_yearly12 = np.zeros((len(years)))
    # Grass_AG_energy_yearly12 = np.zeros((len(years)))
    # Algae_AG_energy_yearly12 = np.zeros((len(years)))
    # Total_energy12 = np.zeros((len(years)))
    # Percentage12 = np.zeros((len(years)))
    
    
    # for year in years:
    #     i = years.index(year)
    #     Y12 = C_yield[:,i]   # corn yield kg/ha
    #     S12 = S_yield[:,i]   # soy yield kg/ha
    #     G12 = G_yield[:,i]   # grass yield kg/ha
    #     A12 = A_yield[:,i]   # algae yield kg/ha
    #     G_L12 = G_yield_L[:,i]   # grass yield kg/ha
    #     A_L12 = A_yield_L[:,i]   # algae yield kg/ha
        
    #     Corn_kg12 = C_ha_AG12.reshape(-1)*Y12.reshape(-1) 
    #     Corn_ethanol_con12 = sum(Corn_kg12*9.42)   #MJ/kg
    #     Corn_energy_yearly12[i] =Corn_ethanol_con12
        
    #     Soy_kg12 = S_ha_AG12.reshape(-1)*S12.reshape(-1)
    #     Soy_Oil_con12 = sum(Soy_kg12*8.02)   #MJ/kg
    #     Soy_energy_yearly12[i] =Soy_Oil_con12
        
    #     Grass_kg12 = G_ha_ML12.reshape(-1)*G12.reshape(-1)
    #     Biocrude_con12 = sum(Grass_kg12*8.35)   #MJ/kg
    #     Grass_energy_yearly12[i] =Biocrude_con12
        
    #     Algae_kg12 = A_ha_ML12.reshape(-1)*A12.reshape(-1)
    #     Algal_Oil_con12 = sum(Algae_kg12*20.82)   #MJ/kg
    #     Algae_energy_yearly12[i] =Algal_Oil_con12
        
    #     Grass_AG_kg12 = G_ha_AG12.reshape(-1)*G_L12.reshape(-1)
    #     Biocrude_con_AG12 = sum(Grass_AG_kg12*8.35)   #MJ/kg
    #     Grass_AG_energy_yearly12[i] =Biocrude_con_AG12
        
    #     Algae_AG_kg12 = A_ha_AG12.reshape(-1)*A_L12.reshape(-1)
    #     Algal_Oil_con_AG12 = sum(Algae_AG_kg12*20.82)   #MJ/kg
    #     Algae_AG_energy_yearly12[i] =Algal_Oil_con_AG12
        
    #     Total12 = Corn_ethanol_con12 + Soy_Oil_con12 + Biocrude_con12 + Algal_Oil_con12 + Biocrude_con_AG12 + Algal_Oil_con_AG12
    #     bg12 = 12 ## We will try 0, 3, 6, 9, 12, 15, 18, 20
    #     bgg12 =  bg12*10**9
    #     con12 = 30.81*(1/0.2641)  ## MJ/litre * liter/gallons
    #     quota12 = bgg12*con12  ## energy as MJ/yr
    #     Total_energy12[i] = Total12 - quota12
    #     Percentage12[i] = Total_energy12[i]*100/quota12
    
    # plt.plot(range(1998,2014),Percentage12, label="12 billion")

    
    
    # ### 15 billion ###
    
    # fn_ha15 = 'Decision_Variables_borg_crops_GHG15' + v + '_PARETO'  +'.csv'
    # df_ha15 = pd.read_csv(fn_ha15,header=0,index_col=0)
    
    # fn15 = 'Objective_functions_borg_crops_GHG15' + v + '_PARETO'  +'.csv'
    # df_O15 = pd.read_csv(fn15,header=0,index_col=0)

    
    # df_O15.columns = ['cost','max_energy_shortfall','min_GHG_emission']
    # sorting15 = df_O15.sort_values(by= objective, ascending=True).head(1)
    
    
    # my_index15 = list(sorting15.index)
    # df_ha15_sorted = df_ha15.loc[my_index15]
    
    # C_ha_AG15 = (np.transpose(df_ha15_sorted).iloc[0:num_c].values)/2 # used hectare for corn 
    # S_ha_AG15 = (np.transpose(df_ha15_sorted).iloc[0:num_c].values)/2 # used hectare for soy
    # G_ha_ML15 = (np.transpose(df_ha15_sorted).iloc[num_c:2*num_c].values) # used hectare for grass
    # A_ha_ML15 = (np.transpose(df_ha15_sorted).iloc[2*num_c:3*num_c].values) # used hectare for algae
    # G_ha_AG15 = (np.transpose(df_ha15_sorted).iloc[3*num_c:4*num_c].values) # used hectare for grass
    # A_ha_AG15 = (np.transpose(df_ha15_sorted).iloc[4*num_c:].values) # used hectare for algae
    
    
    # Corn_energy_yearly15 = np.zeros((len(years)))
    # Soy_energy_yearly15 = np.zeros((len(years)))
    # Grass_energy_yearly15 = np.zeros((len(years)))
    # Algae_energy_yearly15 = np.zeros((len(years)))
    # Grass_AG_energy_yearly15 = np.zeros((len(years)))
    # Algae_AG_energy_yearly15 = np.zeros((len(years)))
    # Total_energy15 = np.zeros((len(years)))
    # Percentage15 = np.zeros((len(years)))
    
    
    # for year in years:
    #     i = years.index(year)
    #     Y15 = C_yield[:,i]   # corn yield kg/ha
    #     S15 = S_yield[:,i]   # soy yield kg/ha
    #     G15 = G_yield[:,i]   # grass yield kg/ha
    #     A15 = A_yield[:,i]   # algae yield kg/ha
    #     G_L15 = G_yield_L[:,i]   # grass yield kg/ha
    #     A_L15 = A_yield_L[:,i]   # algae yield kg/ha
        
    #     Corn_kg15 = C_ha_AG15.reshape(-1)*Y15.reshape(-1) 
    #     Corn_ethanol_con15 = sum(Corn_kg15*9.42)   #MJ/kg
    #     Corn_energy_yearly15[i] =Corn_ethanol_con15
        
    #     Soy_kg15 = S_ha_AG15.reshape(-1)*S15.reshape(-1)
    #     Soy_Oil_con15 = sum(Soy_kg15*8.02)   #MJ/kg
    #     Soy_energy_yearly15[i] =Soy_Oil_con15
        
    #     Grass_kg15 = G_ha_ML15.reshape(-1)*G15.reshape(-1)
    #     Biocrude_con15 = sum(Grass_kg15*8.35)   #MJ/kg
    #     Grass_energy_yearly15[i] =Biocrude_con15
        
    #     Algae_kg15 = A_ha_ML15.reshape(-1)*A15.reshape(-1)
    #     Algal_Oil_con15 = sum(Algae_kg15*20.82)   #MJ/kg
    #     Algae_energy_yearly15[i] =Algal_Oil_con15
        
    #     Grass_AG_kg15 = G_ha_AG15.reshape(-1)*G_L15.reshape(-1)
    #     Biocrude_con_AG15 = sum(Grass_AG_kg15*8.35)   #MJ/kg
    #     Grass_AG_energy_yearly15[i] =Biocrude_con_AG15
        
    #     Algae_AG_kg15 = A_ha_AG15.reshape(-1)*A_L15.reshape(-1)
    #     Algal_Oil_con_AG15 = sum(Algae_AG_kg15*20.82)   #MJ/kg
    #     Algae_AG_energy_yearly15[i] =Algal_Oil_con_AG15
        
    #     Total15 = Corn_ethanol_con15 + Soy_Oil_con15 + Biocrude_con15 + Algal_Oil_con15 + Biocrude_con_AG15 + Algal_Oil_con_AG15
    #     bg15 = 15 ## We will try 0, 3, 6, 9, 12, 15, 18, 20
    #     bgg15 =  bg15*10**9
    #     con15 = 30.81*(1/0.2641)  ## MJ/litre * liter/gallons
    #     quota15 = bgg15*con15  ## energy as MJ/yr
    #     Total_energy15[i] = Total15 - quota15
    #     Percentage15[i] = Total_energy15[i]*100/quota15
    
    # plt.plot(range(1998,2014),Percentage15, label="15 billion")

    
    # ### 18 billion ###
    
    # fn_ha18 = 'Decision_Variables_borg_crops_GHG18' + v + '_PARETO'  +'.csv'
    # df_ha18 = pd.read_csv(fn_ha18,header=0,index_col=0)
    
    # fn18 = 'Objective_functions_borg_crops_GHG18' + v + '_PARETO'  +'.csv'
    # df_O18 = pd.read_csv(fn18,header=0,index_col=0)

    
    # df_O18.columns = ['cost','max_energy_shortfall','min_GHG_emission']
    # sorting18 = df_O18.sort_values(by= objective, ascending=True).head(1)
    
    
    # my_index18 = list(sorting18.index)
    # df_ha18_sorted = df_ha18.loc[my_index18]
    
    # C_ha_AG18 = (np.transpose(df_ha18_sorted).iloc[0:num_c].values)/2 # used hectare for corn 
    # S_ha_AG18 = (np.transpose(df_ha18_sorted).iloc[0:num_c].values)/2 # used hectare for soy
    # G_ha_ML18 = (np.transpose(df_ha18_sorted).iloc[num_c:2*num_c].values) # used hectare for grass
    # A_ha_ML18 = (np.transpose(df_ha18_sorted).iloc[2*num_c:3*num_c].values) # used hectare for algae
    # G_ha_AG18 = (np.transpose(df_ha18_sorted).iloc[3*num_c:4*num_c].values) # used hectare for grass
    # A_ha_AG18 = (np.transpose(df_ha18_sorted).iloc[4*num_c:].values) # used hectare for algae
    
    
    # Corn_energy_yearly18 = np.zeros((len(years)))
    # Soy_energy_yearly18 = np.zeros((len(years)))
    # Grass_energy_yearly18 = np.zeros((len(years)))
    # Algae_energy_yearly18 = np.zeros((len(years)))
    # Grass_AG_energy_yearly18 = np.zeros((len(years)))
    # Algae_AG_energy_yearly18 = np.zeros((len(years)))
    # Total_energy18 = np.zeros((len(years)))
    # Percentage18 = np.zeros((len(years)))
    
    # for year in years:
    #     i = years.index(year)
    #     Y18 = C_yield[:,i]   # corn yield kg/ha
    #     S18 = S_yield[:,i]   # soy yield kg/ha
    #     G18 = G_yield[:,i]   # grass yield kg/ha
    #     A18 = A_yield[:,i]   # algae yield kg/ha
    #     G_L18 = G_yield_L[:,i]   # grass yield kg/ha
    #     A_L18 = A_yield_L[:,i]   # algae yield kg/ha
        
    #     Corn_kg18 = C_ha_AG18.reshape(-1)*Y18.reshape(-1) 
    #     Corn_ethanol_con18 = sum(Corn_kg18*9.42)   #MJ/kg
    #     Corn_energy_yearly18[i] =Corn_ethanol_con18
        
    #     Soy_kg18 = S_ha_AG18.reshape(-1)*S18.reshape(-1)
    #     Soy_Oil_con18 = sum(Soy_kg18*8.02)   #MJ/kg
    #     Soy_energy_yearly18[i] =Soy_Oil_con18
        
    #     Grass_kg18 = G_ha_ML18.reshape(-1)*G18.reshape(-1)
    #     Biocrude_con18 = sum(Grass_kg18*8.35)   #MJ/kg
    #     Grass_energy_yearly18[i] =Biocrude_con18
        
    #     Algae_kg18 = A_ha_ML18.reshape(-1)*A18.reshape(-1)
    #     Algal_Oil_con18 = sum(Algae_kg18*20.82)   #MJ/kg
    #     Algae_energy_yearly18[i] =Algal_Oil_con18
        
    #     Grass_AG_kg18 = G_ha_AG18.reshape(-1)*G_L18.reshape(-1)
    #     Biocrude_con_AG18 = sum(Grass_AG_kg18*8.35)   #MJ/kg
    #     Grass_AG_energy_yearly18[i] =Biocrude_con_AG18
        
    #     Algae_AG_kg18 = A_ha_AG18.reshape(-1)*A_L18.reshape(-1)
    #     Algal_Oil_con_AG18 = sum(Algae_AG_kg18*20.82)   #MJ/kg
    #     Algae_AG_energy_yearly18[i] =Algal_Oil_con_AG18
        
    #     Total18 = Corn_ethanol_con18 + Soy_Oil_con18 + Biocrude_con18 + Algal_Oil_con18 + Biocrude_con_AG18 + Algal_Oil_con_AG18
    #     bg18 = 18 ## We will try 0, 3, 6, 9, 12, 15, 18, 20
    #     bgg18 =  bg18*10**9
    #     con18 = 30.81*(1/0.2641)  ## MJ/litre * liter/gallons
    #     quota18 = bgg18*con18  ## energy as MJ/yr
    #     Total_energy18[i] = Total18 - quota18
    #     Percentage18[i] = Total_energy18[i]*100/quota18
    
    # plt.plot(range(1998,2014),Percentage18, label="18 billion")
    
    # ### 20 billion ###
    
    # fn_ha20 = 'Decision_Variables_borg_crops_GHG20' + v + '_PARETO'  +'.csv'
    # df_ha20 = pd.read_csv(fn_ha20,header=0,index_col=0)
    
    # fn20 = 'Objective_functions_borg_crops_GHG20' + v + '_PARETO'  +'.csv'
    # df_O20 = pd.read_csv(fn20,header=0,index_col=0)
    
    # df_O20.columns = ['cost','max_energy_shortfall','min_GHG_emission']
    # sorting20 = df_O20.sort_values(by= objective, ascending=True).head(1)
    
    # my_index20 = list(sorting20.index)
    # df_ha20_sorted = df_ha20.loc[my_index20]
    
    # C_ha_AG20 = (np.transpose(df_ha20_sorted).iloc[0:num_c].values)/2 # used hectare for corn 
    # S_ha_AG20 = (np.transpose(df_ha20_sorted).iloc[0:num_c].values)/2 # used hectare for soy
    # G_ha_ML20 = (np.transpose(df_ha20_sorted).iloc[num_c:2*num_c].values) # used hectare for grass
    # A_ha_ML20 = (np.transpose(df_ha20_sorted).iloc[2*num_c:3*num_c].values) # used hectare for algae
    # G_ha_AG20 = (np.transpose(df_ha20_sorted).iloc[3*num_c:4*num_c].values) # used hectare for grass
    # A_ha_AG20 = (np.transpose(df_ha20_sorted).iloc[4*num_c:].values) # used hectare for algae
    
    # Corn_energy_yearly20 = np.zeros((len(years)))
    # Soy_energy_yearly20 = np.zeros((len(years)))
    # Grass_energy_yearly20 = np.zeros((len(years)))
    # Algae_energy_yearly20 = np.zeros((len(years)))
    # Grass_AG_energy_yearly20 = np.zeros((len(years)))
    # Algae_AG_energy_yearly20 = np.zeros((len(years)))
    # Total_energy20 = np.zeros((len(years)))
    # Total_p20 = np.zeros((len(years)))
    # Percentage20 = np.zeros((len(years)))
    
    # for year in years:
    #     i = years.index(year)
    #     Y20 = C_yield[:,i]   # corn yield kg/ha
    #     S20 = S_yield[:,i]   # soy yield kg/ha
    #     G20 = G_yield[:,i]   # grass yield kg/ha
    #     A20 = A_yield[:,i]   # algae yield kg/ha
    #     G_L20 = G_yield_L[:,i]   # grass yield kg/ha
    #     A_L20 = A_yield_L[:,i]   # algae yield kg/ha
        
    #     Corn_kg20 = C_ha_AG20.reshape(-1)*Y20.reshape(-1) 
    #     Corn_ethanol_con20 = sum(Corn_kg20*9.42)   #MJ/kg
    #     Corn_energy_yearly20[i] =Corn_ethanol_con20
        
    #     Soy_kg20 = S_ha_AG20.reshape(-1)*S20.reshape(-1) 
    #     Soy_Oil_con20 = sum(Soy_kg20*8.02)   #MJ/kg
    #     Soy_energy_yearly20[i] =Soy_Oil_con20
        
    #     Grass_kg20 = G_ha_ML20.reshape(-1)*G20.reshape(-1)
    #     Biocrude_con20 = sum(Grass_kg20*8.35)   #MJ/kg
    #     Grass_energy_yearly20[i] =Biocrude_con20
        
    #     Algae_kg20 = A_ha_ML20.reshape(-1)*A20.reshape(-1)
    #     Algal_Oil_con20 = sum(Algae_kg20*20.82)   #MJ/kg
    #     Algae_energy_yearly20[i] =Algal_Oil_con20
        
    #     Grass_AG_kg20 = G_ha_AG20.reshape(-1)*G_L20.reshape(-1)
    #     Biocrude_con_AG20 = sum(Grass_AG_kg20*8.35)   #MJ/kg
    #     Grass_AG_energy_yearly20[i] =Biocrude_con_AG20
        
    #     Algae_AG_kg20 = A_ha_AG20.reshape(-1)*A_L20.reshape(-1)
    #     Algal_Oil_con_AG20 = sum(Algae_AG_kg20*20.82)   #MJ/kg
    #     Algae_AG_energy_yearly20[i] =Algal_Oil_con_AG20
        
    #     Total20 = (Corn_ethanol_con20 + Soy_Oil_con20 + Biocrude_con20 + Algal_Oil_con20 + Biocrude_con_AG20 + Algal_Oil_con_AG20)
    #     bg20 = 20 ## We will try 0, 3, 6, 9, 12, 15, 18, 20
    #     bgg20 =  bg20*10**9
    #     con20 = 30.81*(1/0.2641)  ## MJ/litre * liter/gallons
    #     quota20 = bgg20*con20  ## energy as MJ/yr
    #     Total_p20[i] = Total20
    #     Total_energy20[i] = Total20 - quota20
    #     Percentage20[i] = Total_energy20[i]*100/quota20
        
    # ## Zero line
    
    # Total_energy0 = np.zeros((len(years)))
    # Percentage0 = np.zeros((len(years)))
    
        
    # plt.plot(range(1998,2014),Percentage20, label="20 billion")
    
    # plt.plot(range(1998,2014),Percentage0, color='black', linestyle='dashed')
    
    
    # plt.legend(loc="lower left")
    # plt.xlabel('Years', fontsize=18)
    # plt.ylabel('Percentage (%)', fontsize=18)
    # plt.xticks(fontsize=18, rotation=0)
    # plt.yticks(fontsize=18, rotation=0)
    
    # plt.savefig('Time_series_percentage' + v + '.png',dpi=150, bbox_inches='tight')
    
    
    ######## RESIDUAL ENERGY  ###########
    
    # objective = 'max_energy_shortfall'
    objective = 'cost'

    # 3 billion ###
    
    fn_ha3 = 'Decision_Variables_borg_crops_GHG3' + v + '_PARETO'  +'.csv'
    df_ha3 = pd.read_csv(fn_ha3, header=0, index_col=0)
    
    fn3 = 'Objective_functions_borg_crops_GHG3' + v + '_PARETO'  +'.csv'
    df_O3 = pd.read_csv(fn3, header=0, index_col=0)
    
    df_O3.columns = ['cost','max_energy_shortfall','min_GHG_emission']
    sorting3 = df_O3.sort_values(by= objective, ascending=True).head(1)
    
    
    my_index3 = list(sorting3.index)
    df_ha3_sorted = df_ha3.loc[my_index3]
    
    C_ha_AG3 = (np.transpose(df_ha3_sorted).iloc[0:num_c].values)/2 # used hectare for corn 
    S_ha_AG3 = (np.transpose(df_ha3_sorted).iloc[0:num_c].values)/2 # used hectare for soy
    G_ha_ML3 = (np.transpose(df_ha3_sorted).iloc[num_c:2*num_c].values) # used hectare for grass
    A_ha_ML3 = (np.transpose(df_ha3_sorted).iloc[2*num_c:3*num_c].values) # used hectare for algae
    G_ha_AG3 = (np.transpose(df_ha3_sorted).iloc[3*num_c:4*num_c].values) # used hectare for grass
    A_ha_AG3 = (np.transpose(df_ha3_sorted).iloc[4*num_c:].values) # used hectare for algae
    
    
    Corn_energy_yearly3 = np.zeros((len(years)))
    Soy_energy_yearly3 = np.zeros((len(years)))
    Grass_energy_yearly3 = np.zeros((len(years)))
    Algae_energy_yearly3 = np.zeros((len(years)))
    Grass_AG_energy_yearly3 = np.zeros((len(years)))
    Algae_AG_energy_yearly3 = np.zeros((len(years)))
    Total_energy3 = np.zeros((len(years)))
    Total_p3 = np.zeros((len(years)))
    Percentage3 = np.zeros((len(years)))
    
    for year in years:
        i = years.index(year)
        Y3 = C_yield[:,i]  # corn yield kg/ha
        S3 = S_yield[:,i]   # soy yield kg/ha
        G3 = G_yield[:,i]   # grass yield kg/ha
        A3 = A_yield[:,i]   # algae yield kg/ha
        G_L3 = G_yield_L[:,i]   # grass yield kg/ha
        A_L3 = A_yield_L[:,i]   # algae yield kg/ha
        
        Corn_kg3 = C_ha_AG3.reshape(-1)*Y3.reshape(-1)
        Corn_ethanol_con3 = sum(Corn_kg3*9.42)   #MJ/kg
        Corn_energy_yearly3[i] =Corn_ethanol_con3
        
        Soy_kg3 = S_ha_AG3.reshape(-1)*S3.reshape(-1) 
        Soy_Oil_con3 = sum(Soy_kg3*8.02)   #MJ/kg
        Soy_energy_yearly3[i] =Soy_Oil_con3
        
        Grass_kg3 = G_ha_ML3.reshape(-1)*G3.reshape(-1)
        Biocrude_con3 = sum(Grass_kg3*8.35)   #MJ/kg
        Grass_energy_yearly3[i] =Biocrude_con3
        
        Algae_kg3 = A_ha_ML3.reshape(-1)*A3.reshape(-1)
        Algal_Oil_con3 = sum(Algae_kg3*20.82)   #MJ/kg
        Algae_energy_yearly3[i] =Algal_Oil_con3
        
        Grass_AG_kg3 = G_ha_AG3.reshape(-1)*G_L3.reshape(-1)
        Biocrude_con_AG3 = sum(Grass_AG_kg3*8.35)   #MJ/kg
        Grass_AG_energy_yearly3[i] =Biocrude_con_AG3
        
        Algae_AG_kg3 = A_ha_AG3.reshape(-1)*A_L3.reshape(-1)
        Algal_Oil_con_AG3 = sum(Algae_AG_kg3*20.82)   #MJ/kg
        Algae_AG_energy_yearly3[i] =Algal_Oil_con_AG3
        
        Total3 = Corn_ethanol_con3 + Soy_Oil_con3 + Biocrude_con3 + Algal_Oil_con3 + Biocrude_con_AG3 + Algal_Oil_con_AG3
        bg3 = 3 ## We will try 0, 3, 6, 9, 12, 15, 18, 20
        bgg3 =  bg3*10**9
        con3 = 30.81*(1/0.2641)  ## MJ/litre * liter/gallons
        quota3 = bgg3*con3  ## energy as MJ/yr
        Total_p3[i] = Total3
        Total_energy3[i] = Total3 - quota3
        Percentage3[i] = Total_energy3[i]*100/quota3
    
    plt.plot(range(1998,2014),Total_energy3, label="3 billion")
        
    
    ### 6 billion ###
    
    fn_ha6 = 'Decision_Variables_borg_crops_GHG6' + v + '_PARETO'  +'.csv'
    df_ha6 = pd.read_csv(fn_ha6,header=0,index_col=0)
    
    fn6 = 'Objective_functions_borg_crops_GHG6' + v + '_PARETO'  +'.csv'
    df_O6 = pd.read_csv(fn6,header=0,index_col=0)

    df_O6.columns = ['cost','max_energy_shortfall','min_GHG_emission']
    sorting6 = df_O6.sort_values(by= objective, ascending=True).head(1)
    
    
    my_index6 = list(sorting6.index)
    df_ha6_sorted = df_ha6.loc[my_index6]
    
    C_ha_AG6 = (np.transpose(df_ha6_sorted).iloc[0:num_c].values)/2 # used hectare for corn 
    S_ha_AG6 = (np.transpose(df_ha6_sorted).iloc[0:num_c].values)/2 # used hectare for soy
    G_ha_ML6 = (np.transpose(df_ha6_sorted).iloc[num_c:2*num_c].values) # used hectare for grass
    A_ha_ML6 = (np.transpose(df_ha6_sorted).iloc[2*num_c:3*num_c].values) # used hectare for algae
    G_ha_AG6 = (np.transpose(df_ha6_sorted).iloc[3*num_c:4*num_c].values) # used hectare for grass
    A_ha_AG6 = (np.transpose(df_ha6_sorted).iloc[4*num_c:].values) # used hectare for algae
    
    Corn_energy_yearly6 = np.zeros((len(years)))
    Soy_energy_yearly6 = np.zeros((len(years)))
    Grass_energy_yearly6 = np.zeros((len(years)))
    Algae_energy_yearly6 = np.zeros((len(years)))
    Grass_AG_energy_yearly6 = np.zeros((len(years)))
    Algae_AG_energy_yearly6 = np.zeros((len(years)))
    Total_energy6 = np.zeros((len(years)))
    Percentage6 = np.zeros((len(years)))
    
    for year in years:
        i = years.index(year)
        Y6 = C_yield[:,i]   # corn yield kg/ha
        S6 = S_yield[:,i]   # soy yield kg/ha
        G6 = G_yield[:,i]   # grass yield kg/ha
        A6 = A_yield[:,i]   # algae yield kg/ha
        G_L6 = G_yield_L[:,i]   # grass yield kg/ha
        A_L6 = A_yield_L[:,i]   # algae yield kg/ha
        
        Corn_kg6 = C_ha_AG6.reshape(-1)*Y6.reshape(-1) 
        Corn_ethanol_con6 = sum(Corn_kg6*9.42)   #MJ/kg
        Corn_energy_yearly6[i] =Corn_ethanol_con6
        
        Soy_kg6 = S_ha_AG6.reshape(-1)*S6.reshape(-1)
        Soy_Oil_con6 = sum(Soy_kg6*8.02)   #MJ/kg
        Soy_energy_yearly6[i] =Soy_Oil_con6
        
        Grass_kg6 = G_ha_ML6.reshape(-1)*G6.reshape(-1)
        Biocrude_con6 = sum(Grass_kg6*8.35)   #MJ/kg
        Grass_energy_yearly6[i] =Biocrude_con6
        
        Algae_kg6 = A_ha_ML6.reshape(-1)*A6.reshape(-1)
        Algal_Oil_con6 = sum(Algae_kg6*20.82)   #MJ/kg
        Algae_energy_yearly6[i] =Algal_Oil_con6
        
        Grass_AG_kg6 = G_ha_AG6.reshape(-1)*G_L6.reshape(-1)
        Biocrude_con_AG6 = sum(Grass_AG_kg6*8.35)   #MJ/kg
        Grass_AG_energy_yearly6[i] =Biocrude_con_AG6
        
        Algae_AG_kg6 = A_ha_AG6.reshape(-1)*A_L6.reshape(-1)
        Algal_Oil_con_AG6 = sum(Algae_AG_kg6*20.82)   #MJ/kg
        Algae_AG_energy_yearly6[i] =Algal_Oil_con_AG6
        
        Total6 = Corn_ethanol_con6 + Soy_Oil_con6 + Biocrude_con6 + Algal_Oil_con6 + Biocrude_con_AG6 + Algal_Oil_con_AG6
        bg6 = 6 ## We will try 0, 3, 6, 9, 12, 15, 18, 20
        bgg6 =  bg6*10**9
        con6 = 30.81*(1/0.2641)  ## MJ/litre * liter/gallons
        quota6 = bgg6*con6  ## energy as MJ/yr
        Total_energy6[i] = Total6 - quota6
        Percentage6[i] = Total_energy6[i]*100/quota6
        
    plt.plot(range(1998,2014),Total_energy6, label="6 billion")
    
    
    ### 9 billion ###
    
    fn_ha9 = 'Decision_Variables_borg_crops_GHG9' + v + '_PARETO'  +'.csv'
    df_ha9 = pd.read_csv(fn_ha9,header=0,index_col=0)
    
    fn9 = 'Objective_functions_borg_crops_GHG9' + v + '_PARETO'  +'.csv'
    df_O9 = pd.read_csv(fn9,header=0,index_col=0)
    
    df_O9.columns = ['cost','max_energy_shortfall','min_GHG_emission']
    sorting9 = df_O9.sort_values(by= objective, ascending=True).head(1)
    
    
    my_index9 = list(sorting9.index)
    df_ha9_sorted = df_ha9.loc[my_index9]
    
    
    C_ha_AG9 = (np.transpose(df_ha9_sorted).iloc[0:num_c].values)/2 # used hectare for corn 
    S_ha_AG9 = (np.transpose(df_ha9_sorted).iloc[0:num_c].values)/2 # used hectare for soy
    G_ha_ML9 = (np.transpose(df_ha9_sorted).iloc[num_c:2*num_c].values) # used hectare for grass
    A_ha_ML9 = (np.transpose(df_ha9_sorted).iloc[2*num_c:3*num_c].values) # used hectare for algae
    G_ha_AG9 = (np.transpose(df_ha9_sorted).iloc[3*num_c:4*num_c].values) # used hectare for grass
    A_ha_AG9 = (np.transpose(df_ha9_sorted).iloc[4*num_c:].values) # used hectare for algae
    
    Corn_energy_yearly9 = np.zeros((len(years)))
    Soy_energy_yearly9 = np.zeros((len(years)))
    Grass_energy_yearly9 = np.zeros((len(years)))
    Algae_energy_yearly9 = np.zeros((len(years)))
    Grass_AG_energy_yearly9 = np.zeros((len(years)))
    Algae_AG_energy_yearly9 = np.zeros((len(years)))
    Total_energy9 = np.zeros((len(years)))
    Percentage9 = np.zeros((len(years)))
    
    for year in years:
        i = years.index(year)
        Y9 = C_yield[:,i]   # corn yield kg/ha
        S9 = S_yield[:,i]   # soy yield kg/ha
        G9 = G_yield[:,i]   # grass yield kg/ha
        A9 = A_yield[:,i]   # algae yield kg/ha
        G_L9 = G_yield_L[:,i]   # grass yield kg/ha
        A_L9 = A_yield_L[:,i]   # algae yield kg/ha
        
        Corn_kg9 = C_ha_AG9.reshape(-1)*Y9.reshape(-1) 
        Corn_ethanol_con9 = sum(Corn_kg9*9.42)   #MJ/kg
        Corn_energy_yearly9[i] =Corn_ethanol_con9
        
        Soy_kg9 = S_ha_AG9.reshape(-1)*S9.reshape(-1)
        Soy_Oil_con9 = sum(Soy_kg9*8.02)   #MJ/kg
        Soy_energy_yearly9[i] =Soy_Oil_con9
        
        Grass_kg9 = G_ha_ML9.reshape(-1)*G9.reshape(-1)
        Biocrude_con9 = sum(Grass_kg9*8.35)   #MJ/kg
        Grass_energy_yearly9[i] =Biocrude_con9
        
        Algae_kg9 = A_ha_ML9.reshape(-1)*A9.reshape(-1)
        Algal_Oil_con9 = sum(Algae_kg9*20.82)   #MJ/kg
        Algae_energy_yearly9[i] =Algal_Oil_con9
        
        Grass_AG_kg9 = G_ha_AG9.reshape(-1)*G_L9.reshape(-1)
        Biocrude_con_AG9 = sum(Grass_AG_kg9*8.35)   #MJ/kg
        Grass_AG_energy_yearly9[i] =Biocrude_con_AG9
        
        Algae_AG_kg9 = A_ha_AG9.reshape(-1)*A_L9.reshape(-1)
        Algal_Oil_con_AG9 = sum(Algae_AG_kg9*20.82)   #MJ/kg
        Algae_AG_energy_yearly9[i] =Algal_Oil_con_AG9
        
        Total9 = Corn_ethanol_con9 + Soy_Oil_con9 + Biocrude_con9 + Algal_Oil_con9 + Biocrude_con_AG9 + Algal_Oil_con_AG9
        bg9 = 9 ## We will try 0, 3, 6, 9, 12, 15, 18, 20
        bgg9 =  bg9*10**9
        con9 = 30.81*(1/0.2641)  ## MJ/litre * liter/gallons
        quota9 = bgg9*con9  ## energy as MJ/yr
        Total_energy9[i] = Total9 - quota9
        Percentage9[i] = Total_energy9[i]*100/quota9
    
    plt.plot(range(1998,2014),Total_energy9, label="9 billion")
    
    ### 12 billion ###
    
    fn_ha12 = 'Decision_Variables_borg_crops_GHG12' + v + '_PARETO'  +'.csv'
    df_ha12 = pd.read_csv(fn_ha12,header=0,index_col=0)
    
    fn12 = 'Objective_functions_borg_crops_GHG12' + v + '_PARETO'  +'.csv'
    df_O12 = pd.read_csv(fn12,header=0,index_col=0)
    
    df_O12.columns = ['cost','max_energy_shortfall','min_GHG_emission']
    sorting12 = df_O12.sort_values(by= objective, ascending=True).head(1)
    
    my_index12 = list(sorting12.index)
    df_ha12_sorted = df_ha12.loc[my_index12]
    
    C_ha_AG12 = (np.transpose(df_ha12_sorted).iloc[0:num_c].values)/2 # used hectare for corn 
    S_ha_AG12 = (np.transpose(df_ha12_sorted).iloc[0:num_c].values)/2 # used hectare for soy
    G_ha_ML12 = (np.transpose(df_ha12_sorted).iloc[num_c:2*num_c].values) # used hectare for grass
    A_ha_ML12 = (np.transpose(df_ha12_sorted).iloc[2*num_c:3*num_c].values) # used hectare for algae
    G_ha_AG12 = (np.transpose(df_ha12_sorted).iloc[3*num_c:4*num_c].values) # used hectare for grass
    A_ha_AG12 = (np.transpose(df_ha12_sorted).iloc[4*num_c:].values) # used hectare for algae
    
    Corn_energy_yearly12 = np.zeros((len(years)))
    Soy_energy_yearly12 = np.zeros((len(years)))
    Grass_energy_yearly12 = np.zeros((len(years)))
    Algae_energy_yearly12 = np.zeros((len(years)))
    Grass_AG_energy_yearly12 = np.zeros((len(years)))
    Algae_AG_energy_yearly12 = np.zeros((len(years)))
    Total_energy12 = np.zeros((len(years)))
    Percentage12 = np.zeros((len(years)))
    
    
    for year in years:
        i = years.index(year)
        Y12 = C_yield[:,i]   # corn yield kg/ha
        S12 = S_yield[:,i]   # soy yield kg/ha
        G12 = G_yield[:,i]   # grass yield kg/ha
        A12 = A_yield[:,i]   # algae yield kg/ha
        G_L12 = G_yield_L[:,i]   # grass yield kg/ha
        A_L12 = A_yield_L[:,i]   # algae yield kg/ha
        
        Corn_kg12 = C_ha_AG12.reshape(-1)*Y12.reshape(-1) 
        Corn_ethanol_con12 = sum(Corn_kg12*9.42)   #MJ/kg
        Corn_energy_yearly12[i] =Corn_ethanol_con12
        
        Soy_kg12 = S_ha_AG12.reshape(-1)*S12.reshape(-1)
        Soy_Oil_con12 = sum(Soy_kg12*8.02)   #MJ/kg
        Soy_energy_yearly12[i] =Soy_Oil_con12
        
        Grass_kg12 = G_ha_ML12.reshape(-1)*G12.reshape(-1)
        Biocrude_con12 = sum(Grass_kg12*8.35)   #MJ/kg
        Grass_energy_yearly12[i] =Biocrude_con12
        
        Algae_kg12 = A_ha_ML12.reshape(-1)*A12.reshape(-1)
        Algal_Oil_con12 = sum(Algae_kg12*20.82)   #MJ/kg
        Algae_energy_yearly12[i] =Algal_Oil_con12
        
        Grass_AG_kg12 = G_ha_AG12.reshape(-1)*G_L12.reshape(-1)
        Biocrude_con_AG12 = sum(Grass_AG_kg12*8.35)   #MJ/kg
        Grass_AG_energy_yearly12[i] =Biocrude_con_AG12
        
        Algae_AG_kg12 = A_ha_AG12.reshape(-1)*A_L12.reshape(-1)
        Algal_Oil_con_AG12 = sum(Algae_AG_kg12*20.82)   #MJ/kg
        Algae_AG_energy_yearly12[i] =Algal_Oil_con_AG12
        
        Total12 = Corn_ethanol_con12 + Soy_Oil_con12 + Biocrude_con12 + Algal_Oil_con12 + Biocrude_con_AG12 + Algal_Oil_con_AG12
        bg12 = 12 ## We will try 0, 3, 6, 9, 12, 15, 18, 20
        bgg12 =  bg12*10**9
        con12 = 30.81*(1/0.2641)  ## MJ/litre * liter/gallons
        quota12 = bgg12*con12  ## energy as MJ/yr
        Total_energy12[i] = Total12 - quota12
        Percentage12[i] = Total_energy12[i]*100/quota12
    
    plt.plot(range(1998,2014),Total_energy12, label="12 billion")
    
    
    ### 15 billion ###
    
    fn_ha15 = 'Decision_Variables_borg_crops_GHG15' + v + '_PARETO'  +'.csv'
    df_ha15 = pd.read_csv(fn_ha15,header=0,index_col=0)
    
    fn15 = 'Objective_functions_borg_crops_GHG15' + v + '_PARETO'  +'.csv'
    df_O15 = pd.read_csv(fn15,header=0,index_col=0)
    
    df_O15.columns = ['cost','max_energy_shortfall','min_GHG_emission']
    sorting15 = df_O15.sort_values(by= objective, ascending=True).head(1)
    
    
    my_index15 = list(sorting15.index)
    df_ha15_sorted = df_ha15.loc[my_index15]
    
    C_ha_AG15 = (np.transpose(df_ha15_sorted).iloc[0:num_c].values)/2 # used hectare for corn 
    S_ha_AG15 = (np.transpose(df_ha15_sorted).iloc[0:num_c].values)/2 # used hectare for soy
    G_ha_ML15 = (np.transpose(df_ha15_sorted).iloc[num_c:2*num_c].values) # used hectare for grass
    A_ha_ML15 = (np.transpose(df_ha15_sorted).iloc[2*num_c:3*num_c].values) # used hectare for algae
    G_ha_AG15 = (np.transpose(df_ha15_sorted).iloc[3*num_c:4*num_c].values) # used hectare for grass
    A_ha_AG15 = (np.transpose(df_ha15_sorted).iloc[4*num_c:].values) # used hectare for algae
    
    
    Corn_energy_yearly15 = np.zeros((len(years)))
    Soy_energy_yearly15 = np.zeros((len(years)))
    Grass_energy_yearly15 = np.zeros((len(years)))
    Algae_energy_yearly15 = np.zeros((len(years)))
    Grass_AG_energy_yearly15 = np.zeros((len(years)))
    Algae_AG_energy_yearly15 = np.zeros((len(years)))
    Total_energy15 = np.zeros((len(years)))
    Percentage15 = np.zeros((len(years)))
    
    
    for year in years:
        i = years.index(year)
        Y15 = C_yield[:,i]   # corn yield kg/ha
        S15 = S_yield[:,i]   # soy yield kg/ha
        G15 = G_yield[:,i]   # grass yield kg/ha
        A15 = A_yield[:,i]   # algae yield kg/ha
        G_L15 = G_yield_L[:,i]   # grass yield kg/ha
        A_L15 = A_yield_L[:,i]   # algae yield kg/ha
        
        Corn_kg15 = C_ha_AG15.reshape(-1)*Y15.reshape(-1) 
        Corn_ethanol_con15 = sum(Corn_kg15*9.42)   #MJ/kg
        Corn_energy_yearly15[i] =Corn_ethanol_con15
        
        Soy_kg15 = S_ha_AG15.reshape(-1)*S15.reshape(-1)
        Soy_Oil_con15 = sum(Soy_kg15*8.02)   #MJ/kg
        Soy_energy_yearly15[i] =Soy_Oil_con15
        
        Grass_kg15 = G_ha_ML15.reshape(-1)*G15.reshape(-1)
        Biocrude_con15 = sum(Grass_kg15*8.35)   #MJ/kg
        Grass_energy_yearly15[i] =Biocrude_con15
        
        Algae_kg15 = A_ha_ML15.reshape(-1)*A15.reshape(-1)
        Algal_Oil_con15 = sum(Algae_kg15*20.82)   #MJ/kg
        Algae_energy_yearly15[i] =Algal_Oil_con15
        
        Grass_AG_kg15 = G_ha_AG15.reshape(-1)*G_L15.reshape(-1)
        Biocrude_con_AG15 = sum(Grass_AG_kg15*8.35)   #MJ/kg
        Grass_AG_energy_yearly15[i] =Biocrude_con_AG15
        
        Algae_AG_kg15 = A_ha_AG15.reshape(-1)*A_L15.reshape(-1)
        Algal_Oil_con_AG15 = sum(Algae_AG_kg15*20.82)   #MJ/kg
        Algae_AG_energy_yearly15[i] =Algal_Oil_con_AG15
        
        Total15 = Corn_ethanol_con15 + Soy_Oil_con15 + Biocrude_con15 + Algal_Oil_con15 + Biocrude_con_AG15 + Algal_Oil_con_AG15
        bg15 = 15 ## We will try 0, 3, 6, 9, 12, 15, 18, 20
        bgg15 =  bg15*10**9
        con15 = 30.81*(1/0.2641)  ## MJ/litre * liter/gallons
        quota15 = bgg15*con15  ## energy as MJ/yr
        Total_energy15[i] = Total15 - quota15
        Percentage15[i] = Total_energy15[i]*100/quota15

    plt.plot(range(1998,2014),Total_energy15, label="15 billion")
    
    ### 18 billion ###
    
    fn_ha18 = 'Decision_Variables_borg_crops_GHG18' + v + '_PARETO'  +'.csv'
    df_ha18 = pd.read_csv(fn_ha18,header=0,index_col=0)
    
    fn18 = 'Objective_functions_borg_crops_GHG18' + v + '_PARETO'  +'.csv'
    df_O18 = pd.read_csv(fn18,header=0,index_col=0)
    
    df_O18.columns = ['cost','max_energy_shortfall','min_GHG_emission']
    sorting18 = df_O18.sort_values(by= objective, ascending=True).head(1)
    
    
    my_index18 = list(sorting18.index)
    df_ha18_sorted = df_ha18.loc[my_index18]
    
    C_ha_AG18 = (np.transpose(df_ha18_sorted).iloc[0:num_c].values)/2 # used hectare for corn 
    S_ha_AG18 = (np.transpose(df_ha18_sorted).iloc[0:num_c].values)/2 # used hectare for soy
    G_ha_ML18 = (np.transpose(df_ha18_sorted).iloc[num_c:2*num_c].values) # used hectare for grass
    A_ha_ML18 = (np.transpose(df_ha18_sorted).iloc[2*num_c:3*num_c].values) # used hectare for algae
    G_ha_AG18 = (np.transpose(df_ha18_sorted).iloc[3*num_c:4*num_c].values) # used hectare for grass
    A_ha_AG18 = (np.transpose(df_ha18_sorted).iloc[4*num_c:].values) # used hectare for algae
    
    
    Corn_energy_yearly18 = np.zeros((len(years)))
    Soy_energy_yearly18 = np.zeros((len(years)))
    Grass_energy_yearly18 = np.zeros((len(years)))
    Algae_energy_yearly18 = np.zeros((len(years)))
    Grass_AG_energy_yearly18 = np.zeros((len(years)))
    Algae_AG_energy_yearly18 = np.zeros((len(years)))
    Total_energy18 = np.zeros((len(years)))
    Percentage18 = np.zeros((len(years)))
    
    for year in years:
        i = years.index(year)
        Y18 = C_yield[:,i]   # corn yield kg/ha
        S18 = S_yield[:,i]   # soy yield kg/ha
        G18 = G_yield[:,i]   # grass yield kg/ha
        A18 = A_yield[:,i]   # algae yield kg/ha
        G_L18 = G_yield_L[:,i]   # grass yield kg/ha
        A_L18 = A_yield_L[:,i]   # algae yield kg/ha
        
        Corn_kg18 = C_ha_AG18.reshape(-1)*Y18.reshape(-1) 
        Corn_ethanol_con18 = sum(Corn_kg18*9.42)   #MJ/kg
        Corn_energy_yearly18[i] =Corn_ethanol_con18
        
        Soy_kg18 = S_ha_AG18.reshape(-1)*S18.reshape(-1)
        Soy_Oil_con18 = sum(Soy_kg18*8.02)   #MJ/kg
        Soy_energy_yearly18[i] =Soy_Oil_con18
        
        Grass_kg18 = G_ha_ML18.reshape(-1)*G18.reshape(-1)
        Biocrude_con18 = sum(Grass_kg18*8.35)   #MJ/kg
        Grass_energy_yearly18[i] =Biocrude_con18
        
        Algae_kg18 = A_ha_ML18.reshape(-1)*A18.reshape(-1)
        Algal_Oil_con18 = sum(Algae_kg18*20.82)   #MJ/kg
        Algae_energy_yearly18[i] =Algal_Oil_con18
        
        Grass_AG_kg18 = G_ha_AG18.reshape(-1)*G_L18.reshape(-1)
        Biocrude_con_AG18 = sum(Grass_AG_kg18*8.35)   #MJ/kg
        Grass_AG_energy_yearly18[i] =Biocrude_con_AG18
        
        Algae_AG_kg18 = A_ha_AG18.reshape(-1)*A_L18.reshape(-1)
        Algal_Oil_con_AG18 = sum(Algae_AG_kg18*20.82)   #MJ/kg
        Algae_AG_energy_yearly18[i] =Algal_Oil_con_AG18
        
        Total18 = Corn_ethanol_con18 + Soy_Oil_con18 + Biocrude_con18 + Algal_Oil_con18 + Biocrude_con_AG18 + Algal_Oil_con_AG18
        bg18 = 18 ## We will try 0, 3, 6, 9, 12, 15, 18, 20
        bgg18 =  bg18*10**9
        con18 = 30.81*(1/0.2641)  ## MJ/litre * liter/gallons
        quota18 = bgg18*con18  ## energy as MJ/yr
        Total_energy18[i] = Total18 - quota18
        Percentage18[i] = Total_energy18[i]*100/quota18

    plt.plot(range(1998,2014),Total_energy18, label="18 billion")
    
    ### 20 billion ###
    
    fn_ha20 = 'Decision_Variables_borg_crops_GHG20' + v + '_PARETO'  +'.csv'
    df_ha20 = pd.read_csv(fn_ha20,header=0,index_col=0)
    
    fn20 = 'Objective_functions_borg_crops_GHG20' + v + '_PARETO'  +'.csv'
    df_O20 = pd.read_csv(fn20,header=0,index_col=0)
    
    df_O20.columns = ['cost','max_energy_shortfall','min_GHG_emission']
    sorting20 = df_O20.sort_values(by= objective, ascending=True).head(1)
    
    my_index20 = list(sorting20.index)
    df_ha20_sorted = df_ha20.loc[my_index20]
    
    C_ha_AG20 = (np.transpose(df_ha20_sorted).iloc[0:num_c].values)/2 # used hectare for corn 
    S_ha_AG20 = (np.transpose(df_ha20_sorted).iloc[0:num_c].values)/2 # used hectare for soy
    G_ha_ML20 = (np.transpose(df_ha20_sorted).iloc[num_c:2*num_c].values) # used hectare for grass
    A_ha_ML20 = (np.transpose(df_ha20_sorted).iloc[2*num_c:3*num_c].values) # used hectare for algae
    G_ha_AG20 = (np.transpose(df_ha20_sorted).iloc[3*num_c:4*num_c].values) # used hectare for grass
    A_ha_AG20 = (np.transpose(df_ha20_sorted).iloc[4*num_c:].values) # used hectare for algae
    
    Corn_energy_yearly20 = np.zeros((len(years)))
    Soy_energy_yearly20 = np.zeros((len(years)))
    Grass_energy_yearly20 = np.zeros((len(years)))
    Algae_energy_yearly20 = np.zeros((len(years)))
    Grass_AG_energy_yearly20 = np.zeros((len(years)))
    Algae_AG_energy_yearly20 = np.zeros((len(years)))
    Total_energy20 = np.zeros((len(years)))
    Total_p20 = np.zeros((len(years)))
    Percentage20 = np.zeros((len(years)))
    
    for year in years:
        i = years.index(year)
        Y20 = C_yield[:,i]   # corn yield kg/ha
        S20 = S_yield[:,i]   # soy yield kg/ha
        G20 = G_yield[:,i]   # grass yield kg/ha
        A20 = A_yield[:,i]   # algae yield kg/ha
        G_L20 = G_yield_L[:,i]   # grass yield kg/ha
        A_L20 = A_yield_L[:,i]   # algae yield kg/ha
        
        Corn_kg20 = C_ha_AG20.reshape(-1)*Y20.reshape(-1) 
        Corn_ethanol_con20 = sum(Corn_kg20*9.42)   #MJ/kg
        Corn_energy_yearly20[i] =Corn_ethanol_con20
        
        Soy_kg20 = S_ha_AG20.reshape(-1)*S20.reshape(-1) 
        Soy_Oil_con20 = sum(Soy_kg20*8.02)   #MJ/kg
        Soy_energy_yearly20[i] =Soy_Oil_con20
        
        Grass_kg20 = G_ha_ML20.reshape(-1)*G20.reshape(-1)
        Biocrude_con20 = sum(Grass_kg20*8.35)   #MJ/kg
        Grass_energy_yearly20[i] =Biocrude_con20
        
        Algae_kg20 = A_ha_ML20.reshape(-1)*A20.reshape(-1)
        Algal_Oil_con20 = sum(Algae_kg20*20.82)   #MJ/kg
        Algae_energy_yearly20[i] =Algal_Oil_con20
        
        Grass_AG_kg20 = G_ha_AG20.reshape(-1)*G_L20.reshape(-1)
        Biocrude_con_AG20 = sum(Grass_AG_kg20*8.35)   #MJ/kg
        Grass_AG_energy_yearly20[i] =Biocrude_con_AG20
        
        Algae_AG_kg20 = A_ha_AG20.reshape(-1)*A_L20.reshape(-1)
        Algal_Oil_con_AG20 = sum(Algae_AG_kg20*20.82)   #MJ/kg
        Algae_AG_energy_yearly20[i] =Algal_Oil_con_AG20
        
        Total20 = (Corn_ethanol_con20 + Soy_Oil_con20 + Biocrude_con20 + Algal_Oil_con20 + Biocrude_con_AG20 + Algal_Oil_con_AG20)
        bg20 = 20 ## We will try 0, 3, 6, 9, 12, 15, 18, 20
        bgg20 =  bg20*10**9
        con20 = 30.81*(1/0.2641)  ## MJ/litre * liter/gallons
        quota20 = bgg20*con20  ## energy as MJ/yr
        Total_p20[i] = Total20
        Total_energy20[i] = Total20 - quota20
        Percentage20[i] = Total_energy20[i]*100/quota20


    plt.plot(range(1998,2014),Total_energy20, label="20 billion")
    
    ## Zero line
    Total_energy0 = np.zeros((len(years)))
    Percentage0 = np.zeros((len(years)))

    plt.plot(range(1998,2014),Total_energy0, color='black', linestyle='dashed')

    
    plt.legend(loc="lower left")
    plt.xlabel('Years', fontsize=18)
    plt.ylabel('Residual Energy (MJ)', fontsize=18)
    plt.xticks(fontsize=18, rotation=0)
    plt.yticks(fontsize=18, rotation=0)
    
    plt.savefig('Time_series_residual_energy' + v + '.png',dpi=150, bbox_inches='tight')

    
    
    
    
    
    
