# -*- coding: utf-8 -*-
"""
Created on Tue Feb 28 10:38:11 2023

@author: eari
"""

import pandas as pd
import numpy as np


# Yields and land limits : contains State - STASD_N - land_limits_ha - yields (1998-2013)
df_geo_corn = pd.read_excel('combined_pivot_Corn.xlsx',header=0, engine='openpyxl')
df_geo_grass_AG = pd.read_excel('combined_pivot_AG_Switchgrass.xlsx',header=0, engine='openpyxl') 
df_geo_grass_ML = pd.read_excel('combined_pivot_ML_Switchgrass.xlsx',header=0, engine='openpyxl') 
df_geo_algae_AG = pd.read_excel('combined_pivot_AG_Algae.xlsx',header=0, engine='openpyxl')   
df_geo_algae_ML = pd.read_excel('combined_pivot_ML_Algae.xlsx',header=0, engine='openpyxl')  



States = list(df_geo_corn['State'])
s = pd.Series(np.tile(States,5))

districts = list(df_geo_corn['STASD_N'])
d= pd.Series(np.tile(districts,5))

num_c = int(5*len(df_geo_corn)) #size of land limit

df_total_land_limit = pd.DataFrame(np.zeros((num_c,3)))
df_total_land_limit.columns = ['state','STASD_N','land_limits_ha']


land_limit_AG = pd.DataFrame(df_geo_corn['land_limits_ha'].values)
land_limit_ML_Grass = pd.DataFrame(df_geo_grass_ML['land_limits_ha'].values)
land_limit_ML_Algae = pd.DataFrame(df_geo_algae_ML['land_limits_ha'].values)
land_limit_AG_Grass = pd.DataFrame(df_geo_corn['land_limits_ha'].values)
land_limit_AG_Algae = pd.DataFrame(df_geo_corn['land_limits_ha'].values)

frames = [land_limit_AG, land_limit_ML_Grass, land_limit_ML_Algae, land_limit_AG_Grass, land_limit_AG_Algae]
  
result = pd.concat(frames)
result.reset_index(drop=True, inplace=True)


df_total_land_limit['state'] = s
df_total_land_limit['STASD_N'] = d
df_total_land_limit['land_limits_ha'] = result

df_total_land_limit.to_excel('total_land_limit.xlsx', engine='openpyxl')

