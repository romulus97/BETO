# -*- coding: utf-8 -*-
"""
Created on Thu Oct 28 20:03:00 2021

@author: Ece Ari Akdemir
"""

from platypus import GDE3, Problem, Real
from pyborg import BorgMOEA
import random
from random import randint
import pandas as pd
import numpy as np
import time

start = time.time()
version = 'district'

#####################################################################
##########           IMPORT DATA           ##########################
#####################################################################

# Yields and land limits : contains State - STASD_N - land_limits_ha - yields (1998-2013)
df_geo_corn = pd.read_excel('Data/combined_pivot_Corn.xlsx',header=0, engine='openpyxl')
del df_geo_corn['Unnamed: 0']
df_geo_soy = pd.read_excel('Data/combined_pivot_Soy.xlsx',header=0, engine='openpyxl')
del df_geo_soy['Unnamed: 0']
df_geo_grass_AG = pd.read_excel('Data/combined_pivot_AG_Switchgrass.xlsx',header=0, engine='openpyxl') 
del df_geo_grass_AG['Unnamed: 0']
df_geo_grass_ML = pd.read_excel('Data/combined_pivot_ML_Switchgrass.xlsx',header=0, engine='openpyxl') 
del df_geo_grass_ML['Unnamed: 0']
df_geo_algae_AG = pd.read_excel('Data/combined_pivot_AG_Algae.xlsx',header=0, engine='openpyxl')  
del df_geo_algae_AG['Unnamed: 0'] 
df_geo_algae_ML = pd.read_excel('Data/combined_pivot_ML_Algae.xlsx',header=0, engine='openpyxl')  
del df_geo_algae_ML['Unnamed: 0']

# Greenhouse gas emission : contains State - STASD_N - greenhouse gas emission (gCO2/MJ) (1998-2013)
df_geo_corn_GHG= pd.read_excel('Data/Corn_GHG.xlsx',header=0, engine='openpyxl') 
df_geo_soy_GHG = pd.read_excel('Data/Soy_GHG.xlsx',header=0, engine='openpyxl') 
df_geo_grass_AG_GHG = pd.read_excel('Data/Switchgrass_AG_GHG.xlsx',header=0, engine='openpyxl')
df_geo_grass_ML_GHG = pd.read_excel('Data/Switchgrass_ML_GHG.xlsx',header=0, engine='openpyxl') 
df_geo_algae_AG_GHG = pd.read_excel('Data/Algae_AG_GHG.xlsx',header=0, engine='openpyxl')
df_geo_algae_ML_GHG = pd.read_excel('Data/Algae_ML_GHG.xlsx',header=0, engine='openpyxl')

# Minimum fuel selling price (MFSP) : contains State - STASD_N - MFSP ($/MJ) (1998-2013)
df_geo_corn_MFSP = pd.read_excel('Data/Corn_MFSP.xlsx',header=0, engine='openpyxl')
df_geo_soy_MFSP = pd.read_excel('Data/Soy_MFSP.xlsx',header=0, engine='openpyxl')
df_geo_grass_AG_MFSP = pd.read_excel('Data/Switchgrass_AG_MFSP.xlsx',header=0, engine='openpyxl') 
df_geo_grass_ML_MFSP = pd.read_excel('Data/Switchgrass_ML_MFSP.xlsx',header=0, engine='openpyxl')
df_geo_algae_AG_MFSP = pd.read_excel('Data/Algae_AG_MFSP.xlsx',header=0, engine='openpyxl')
df_geo_algae_ML_MFSP = pd.read_excel('Data/Algae_ML_MFSP.xlsx',header=0, engine='openpyxl')

state = df_geo_corn['State'].unique()
years = list(range(1998,2014))

ILLINOIS_clusters = [[1710,1720,1730],[1740,1750,1760],[1770,1780,1790]]
INDIANA_clusters = [[1810,1820,1830],[1840,1850,1860],[1870,1880,1890]]
IOWA_clusters = [[1910,1920,1930],[1940,1950,1960],[1970,1980,1990]]
KANSAS_clusters = [[2010,2020,2030],[2040,2050,2060],[2070,2080,2090]]
MICHIGAN_clusters = [[2610,2620,2630],[2640,2650,2660],[2670,2680,2690]]
MINNESOTA_clusters = [[2710,2720,2730],[2740,2750,2760],[2770,2780,2790]]
MISSOURI_clusters = [[2910,2920,2930],[2940,2950,2960],[2970,2980,2990]]
NEBRASKA_clusters = [[3110,3120,3130],[3150,3160],[3170,3180,3190]]
NORTH_DAKOTA_clusters = [[3810,3820,3830],[3840,3850,3860],[3870,3880,3890]]
OHIO_clusters = [[3910,3920,3930],[3940,3950,3960],[3970,3980,3990]]
SOUTH_DAKOTA_clusters = [[4610,4620,4630],[4640,4650,4660],[4670,4680,4690]]
WISCONSIN_clusters = [[5510,5520,5530],[5540,5550,5560],[5570,5580,5590]]
number_cluster = len(ILLINOIS_clusters)

row_num = int(108/number_cluster-1)

df_geo_corn_new = pd.DataFrame(np.zeros((row_num,len(df_geo_corn.columns))),columns=df_geo_corn.columns)
df_geo_soy_new = pd.DataFrame(np.zeros((row_num,len(df_geo_soy.columns))),columns=df_geo_soy.columns)
df_geo_grass_AG_new = pd.DataFrame(np.zeros((row_num,len(df_geo_grass_AG.columns))),columns=df_geo_grass_AG.columns)
df_geo_grass_ML_new = pd.DataFrame(np.zeros((row_num,len(df_geo_grass_ML.columns))),columns=df_geo_grass_ML.columns)
df_geo_algae_AG_new = pd.DataFrame(np.zeros((row_num,len(df_geo_algae_AG.columns))),columns=df_geo_algae_AG.columns)
df_geo_algae_ML_new = pd.DataFrame(np.zeros((row_num,len(df_geo_algae_ML.columns))),columns=df_geo_algae_ML.columns) 


df_geo_corn_GHG_new = pd.DataFrame(np.zeros((row_num,len(df_geo_corn_GHG.columns))),columns=df_geo_corn_GHG.columns)
df_geo_soy_GHG_new = pd.DataFrame(np.zeros((row_num,len(df_geo_soy_GHG.columns))),columns=df_geo_soy_GHG.columns)
df_geo_grass_AG_GHG_new = pd.DataFrame(np.zeros((row_num,len(df_geo_grass_AG_GHG.columns))),columns=df_geo_grass_AG_GHG.columns)
df_geo_grass_ML_GHG_new = pd.DataFrame(np.zeros((row_num,len(df_geo_grass_ML_GHG.columns))),columns=df_geo_grass_ML_GHG.columns)
df_geo_algae_AG_GHG_new = pd.DataFrame(np.zeros((row_num,len(df_geo_algae_AG_GHG.columns))),columns=df_geo_algae_AG_GHG.columns)
df_geo_algae_ML_GHG_new = pd.DataFrame(np.zeros((row_num,len(df_geo_algae_ML_GHG.columns))),columns=df_geo_algae_ML_GHG.columns) 


df_geo_corn_MFSP_new = pd.DataFrame(np.zeros((row_num,len(df_geo_corn_MFSP.columns))),columns=df_geo_corn_MFSP.columns)
df_geo_soy_MFSP_new = pd.DataFrame(np.zeros((row_num,len(df_geo_soy_MFSP.columns))),columns=df_geo_soy_MFSP.columns)
df_geo_grass_AG_MFSP_new = pd.DataFrame(np.zeros((row_num,len(df_geo_grass_AG_MFSP.columns))),columns=df_geo_grass_AG_MFSP.columns)
df_geo_grass_ML_MFSP_new = pd.DataFrame(np.zeros((row_num,len(df_geo_grass_ML_MFSP.columns))),columns=df_geo_grass_ML_MFSP.columns)
df_geo_algae_AG_MFSP_new = pd.DataFrame(np.zeros((row_num,len(df_geo_algae_AG_MFSP.columns))),columns=df_geo_algae_AG_MFSP.columns)
df_geo_algae_ML_MFSP_new = pd.DataFrame(np.zeros((row_num,len(df_geo_algae_ML_MFSP.columns))),columns=df_geo_algae_ML_MFSP.columns) 


index=0
for st in state:
    if st == 'SOUTH DAKOTA':
        cluster_name = 'SOUTH_DAKOTA'
    elif st == 'NORTH DAKOTA':
        cluster_name = 'NORTH_DAKOTA'
    else:
        cluster_name = st
    
    for i in range(0,number_cluster):
        
        my_cluster = globals()[f'{cluster_name}_clusters'][i]
        new_STASD_N = f'{st}_{i}'
        
        selected_df_geo_corn = df_geo_corn.loc[df_geo_corn['STASD_N'].isin(my_cluster)]
        total_land = selected_df_geo_corn['land_limits_ha'].sum()
        mean_vals = selected_df_geo_corn.loc[:,years].mean().values
        df_geo_corn_new.loc[index,'State'] = st
        df_geo_corn_new.loc[index,'STASD_N'] = new_STASD_N
        df_geo_corn_new.loc[index,'land_limits_ha'] = total_land
        df_geo_corn_new.loc[index,years] = mean_vals
        
        selected_df_geo_soy = df_geo_soy.loc[df_geo_soy['STASD_N'].isin(my_cluster)]
        total_land = selected_df_geo_soy['land_limits_ha'].sum()
        mean_vals = selected_df_geo_soy.loc[:,years].mean().values
        df_geo_soy_new.loc[index,'State'] = st
        df_geo_soy_new.loc[index,'STASD_N'] = new_STASD_N
        df_geo_soy_new.loc[index,'land_limits_ha'] = total_land
        df_geo_soy_new.loc[index,years] = mean_vals
        
        selected_df_geo_grass_AG = df_geo_grass_AG.loc[df_geo_grass_AG['STASD_N'].isin(my_cluster)]
        total_land = selected_df_geo_grass_AG['land_limits_ha'].sum()
        mean_vals = selected_df_geo_grass_AG.loc[:,years].mean().values
        df_geo_grass_AG_new.loc[index,'State'] = st
        df_geo_grass_AG_new.loc[index,'STASD_N'] = new_STASD_N
        df_geo_grass_AG_new.loc[index,'land_limits_ha'] = total_land
        df_geo_grass_AG_new.loc[index,years] = mean_vals
        
        selected_df_geo_grass_ML = df_geo_grass_ML.loc[df_geo_grass_ML['STASD_N'].isin(my_cluster)]
        total_land = selected_df_geo_grass_ML['land_limits_ha'].sum()
        mean_vals = selected_df_geo_grass_ML.loc[:,years].mean().values
        df_geo_grass_ML_new.loc[index,'State'] = st
        df_geo_grass_ML_new.loc[index,'STASD_N'] = new_STASD_N
        df_geo_grass_ML_new.loc[index,'land_limits_ha'] = total_land
        df_geo_grass_ML_new.loc[index,years] = mean_vals
        
        selected_df_geo_algae_AG = df_geo_algae_AG.loc[df_geo_algae_AG['STASD_N'].isin(my_cluster)]
        total_land = selected_df_geo_algae_AG['land_limits_ha'].sum()
        mean_vals = selected_df_geo_algae_AG.loc[:,years].mean().values
        df_geo_algae_AG_new.loc[index,'State'] = st
        df_geo_algae_AG_new.loc[index,'STASD_N'] = new_STASD_N
        df_geo_algae_AG_new.loc[index,'land_limits_ha'] = total_land
        df_geo_algae_AG_new.loc[index,years] = mean_vals
        
        selected_df_geo_algae_ML = df_geo_algae_ML.loc[df_geo_algae_ML['STASD_N'].isin(my_cluster)]
        total_land = selected_df_geo_algae_ML['land_limits_ha'].sum()
        mean_vals = selected_df_geo_algae_ML.loc[:,years].mean().values
        df_geo_algae_ML_new.loc[index,'State'] = st
        df_geo_algae_ML_new.loc[index,'STASD_N'] = new_STASD_N
        df_geo_algae_ML_new.loc[index,'land_limits_ha'] = total_land
        df_geo_algae_ML_new.loc[index,years] = mean_vals
        
        
        #GHG
        selected_df_geo_corn_GHG = df_geo_corn_GHG.loc[df_geo_corn_GHG['STASD_N'].isin(my_cluster)]
        mean_vals = selected_df_geo_corn_GHG.loc[:,years].mean().values
        df_geo_corn_GHG_new.loc[index,'State'] = st
        df_geo_corn_GHG_new.loc[index,'STASD_N'] = new_STASD_N
        df_geo_corn_GHG_new.loc[index,years] = mean_vals
        
        selected_df_geo_soy_GHG = df_geo_soy_GHG.loc[df_geo_soy_GHG['STASD_N'].isin(my_cluster)]
        mean_vals = selected_df_geo_soy_GHG.loc[:,years].mean().values
        df_geo_soy_GHG_new.loc[index,'State'] = st
        df_geo_soy_GHG_new.loc[index,'STASD_N'] = new_STASD_N
        df_geo_soy_GHG_new.loc[index,years] = mean_vals
        
        selected_df_geo_grass_AG_GHG = df_geo_grass_AG_GHG.loc[df_geo_grass_AG_GHG['STASD_N'].isin(my_cluster)]
        mean_vals = selected_df_geo_grass_AG_GHG.loc[:,years].mean().values
        df_geo_grass_AG_GHG_new.loc[index,'State'] = st
        df_geo_grass_AG_GHG_new.loc[index,'STASD_N'] = new_STASD_N
        df_geo_grass_AG_GHG_new.loc[index,years] = mean_vals
        
        selected_df_geo_grass_ML_GHG = df_geo_grass_ML_GHG.loc[df_geo_grass_ML_GHG['STASD_N'].isin(my_cluster)]
        mean_vals = selected_df_geo_grass_ML_GHG.loc[:,years].mean().values
        df_geo_grass_ML_GHG_new.loc[index,'State'] = st
        df_geo_grass_ML_GHG_new.loc[index,'STASD_N'] = new_STASD_N
        df_geo_grass_ML_GHG_new.loc[index,years] = mean_vals
        
        selected_df_geo_algae_AG_GHG = df_geo_algae_AG_GHG.loc[df_geo_algae_AG_GHG['STASD_N'].isin(my_cluster)]
        mean_vals = selected_df_geo_algae_AG_GHG.loc[:,years].mean().values
        df_geo_algae_AG_GHG_new.loc[index,'State'] = st
        df_geo_algae_AG_GHG_new.loc[index,'STASD_N'] = new_STASD_N
        df_geo_algae_AG_GHG_new.loc[index,years] = mean_vals
        
        selected_df_geo_algae_ML_GHG = df_geo_algae_ML_GHG.loc[df_geo_algae_ML_GHG['STASD_N'].isin(my_cluster)]
        mean_vals = selected_df_geo_algae_ML_GHG.loc[:,years].mean().values
        df_geo_algae_ML_GHG_new.loc[index,'State'] = st
        df_geo_algae_ML_GHG_new.loc[index,'STASD_N'] = new_STASD_N
        df_geo_algae_ML_GHG_new.loc[index,years] = mean_vals
        
        
        #MFSP
        selected_df_geo_corn_MFSP = df_geo_corn_MFSP.loc[df_geo_corn_MFSP['STASD_N'].isin(my_cluster)]
        mean_vals = selected_df_geo_corn_MFSP.loc[:,years].mean().values
        df_geo_corn_MFSP_new.loc[index,'State'] = st
        df_geo_corn_MFSP_new.loc[index,'STASD_N'] = new_STASD_N
        df_geo_corn_MFSP_new.loc[index,years] = mean_vals
        
        selected_df_geo_soy_MFSP = df_geo_soy_MFSP.loc[df_geo_soy_MFSP['STASD_N'].isin(my_cluster)]
        mean_vals = selected_df_geo_soy_MFSP.loc[:,years].mean().values
        df_geo_soy_MFSP_new.loc[index,'State'] = st
        df_geo_soy_MFSP_new.loc[index,'STASD_N'] = new_STASD_N
        df_geo_soy_MFSP_new.loc[index,years] = mean_vals
        
        selected_df_geo_grass_AG_MFSP = df_geo_grass_AG_MFSP.loc[df_geo_grass_AG_MFSP['STASD_N'].isin(my_cluster)]
        mean_vals = selected_df_geo_grass_AG_MFSP.loc[:,years].mean().values
        df_geo_grass_AG_MFSP_new.loc[index,'State'] = st
        df_geo_grass_AG_MFSP_new.loc[index,'STASD_N'] = new_STASD_N
        df_geo_grass_AG_MFSP_new.loc[index,years] = mean_vals
        
        selected_df_geo_grass_ML_MFSP = df_geo_grass_ML_MFSP.loc[df_geo_grass_ML_MFSP['STASD_N'].isin(my_cluster)]
        mean_vals = selected_df_geo_grass_ML_MFSP.loc[:,years].mean().values
        df_geo_grass_ML_MFSP_new.loc[index,'State'] = st
        df_geo_grass_ML_MFSP_new.loc[index,'STASD_N'] = new_STASD_N
        df_geo_grass_ML_MFSP_new.loc[index,years] = mean_vals
        
        selected_df_geo_algae_AG_MFSP = df_geo_algae_AG_MFSP.loc[df_geo_algae_AG_MFSP['STASD_N'].isin(my_cluster)]
        mean_vals = selected_df_geo_algae_AG_MFSP.loc[:,years].mean().values
        df_geo_algae_AG_MFSP_new.loc[index,'State'] = st
        df_geo_algae_AG_MFSP_new.loc[index,'STASD_N'] = new_STASD_N
        df_geo_algae_AG_MFSP_new.loc[index,years] = mean_vals
        
        selected_df_geo_algae_ML_MFSP = df_geo_algae_ML_MFSP.loc[df_geo_algae_ML_MFSP['STASD_N'].isin(my_cluster)]
        mean_vals = selected_df_geo_algae_ML_MFSP.loc[:,years].mean().values
        df_geo_algae_ML_MFSP_new.loc[index,'State'] = st
        df_geo_algae_ML_MFSP_new.loc[index,'STASD_N'] = new_STASD_N
        df_geo_algae_ML_MFSP_new.loc[index,years] = mean_vals
        
        index += 1
        

        
df_geo_corn_new.to_excel('combined_pivot_Corn.xlsx')
df_geo_soy_new.to_excel('combined_pivot_Soy.xlsx')
df_geo_grass_AG_new.to_excel('combined_pivot_AG_Switchgrass.xlsx')
df_geo_grass_ML_new.to_excel('combined_pivot_ML_Switchgrass.xlsx')
df_geo_algae_AG_new.to_excel('combined_pivot_AG_Algae.xlsx')
df_geo_algae_ML_new.to_excel('combined_pivot_ML_Algae.xlsx')

df_geo_corn_GHG_new.to_excel('Corn_GHG.xlsx')
df_geo_soy_GHG_new.to_excel('Soy_GHG.xlsx')
df_geo_grass_AG_GHG_new.to_excel('Switchgrass_AG_GHG.xlsx')
df_geo_grass_ML_GHG_new.to_excel('Switchgrass_ML_GHG.xlsx')
df_geo_algae_AG_GHG_new.to_excel('Algae_AG_GHG.xlsx')
df_geo_algae_ML_GHG_new.to_excel('Algae_ML_GHG.xlsx')
        
df_geo_corn_MFSP_new.to_excel('Corn_MFSP.xlsx')
df_geo_soy_MFSP_new.to_excel('Soy_MFSP.xlsx')
df_geo_grass_AG_MFSP_new.to_excel('Switchgrass_AG_MFSP.xlsx')
df_geo_grass_ML_MFSP_new.to_excel('Switchgrass_ML_MFSP.xlsx')
df_geo_algae_AG_MFSP_new.to_excel('Algae_AG_MFSP.xlsx')
df_geo_algae_ML_MFSP_new.to_excel('Algae_ML_MFSP.xlsx')
        
    