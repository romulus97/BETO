# -*- coding: utf-8 -*-
"""
Created on Tue Jul 12 15:20:55 2022

@author: eari
"""


version = 'district'

import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import plotly.io as pio
pio.renderers.default='browser'
import contextily
from shapely.geometry import Point, Polygon
import numpy as np
from matplotlib.cm import ScalarMappable
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import TwoSlopeNorm
import geopandas as gpd


df_geo_corn = pd.read_excel('combined_pivot_Corn.xlsx',header=0, engine='openpyxl')
df_geo_soy = pd.read_excel('combined_pivot_Soy.xlsx',header=0, engine='openpyxl')
df_geo_grass_AG = pd.read_excel('combined_pivot_AG_Switchgrass.xlsx',header=0, engine='openpyxl') 
df_geo_grass_ML = pd.read_excel('combined_pivot_ML_Switchgrass.xlsx',header=0, engine='openpyxl') 
df_geo_algae_AG = pd.read_excel('combined_pivot_AG_Algae.xlsx',header=0, engine='openpyxl')   
df_geo_algae_ML = pd.read_excel('combined_pivot_ML_Algae.xlsx',header=0, engine='openpyxl')  


# Greenhouse gas emission : contains State - STASD_N - greenhouse gas emission (gCO2/MJ) (1998-2013)
df_geo_corn_GHG= pd.read_excel('Corn_GHG.xlsx',header=0, engine='openpyxl') 
df_geo_soy_GHG = pd.read_excel('Soy_GHG.xlsx',header=0, engine='openpyxl') 
df_geo_grass_AG_GHG = pd.read_excel('Switchgrass_AG_GHG.xlsx',header=0, engine='openpyxl')
df_geo_grass_ML_GHG = pd.read_excel('Switchgrass_ML_GHG.xlsx',header=0, engine='openpyxl') 
df_geo_algae_AG_GHG = pd.read_excel('Algae_AG_GHG.xlsx',header=0, engine='openpyxl')
df_geo_algae_ML_GHG = pd.read_excel('Algae_ML_GHG.xlsx',header=0, engine='openpyxl')


# Minimum fuel selling price (MFSP) : contains State - STASD_N - MFSP ($/MJ) (1998-2013)
df_geo_corn_MFSP = pd.read_excel('Corn_MFSP.xlsx',header=0, engine='openpyxl')
df_geo_soy_MFSP = pd.read_excel('Soy_MFSP.xlsx',header=0, engine='openpyxl')
df_geo_grass_AG_MFSP = pd.read_excel('Switchgrass_AG_MFSP.xlsx',header=0, engine='openpyxl') 
df_geo_grass_ML_MFSP = pd.read_excel('Switchgrass_ML_MFSP.xlsx',header=0, engine='openpyxl')
df_geo_algae_AG_MFSP = pd.read_excel('Algae_AG_MFSP.xlsx',header=0, engine='openpyxl')
df_geo_algae_ML_MFSP = pd.read_excel('Algae_ML_MFSP.xlsx',header=0, engine='openpyxl')


df = pd.read_csv('AgD_48g_cords_cb.csv',header=0)
years = range(1998,2014)

crs = {'init':'epsg:4326'}

geometry = [Point(xy) for xy in zip(df['Longitude'],df['Latitude'])]
geo_df = gpd.GeoDataFrame(df,crs=crs,geometry=geometry)
geo_df = geo_df.to_crs(epsg=2163)

state_map = gpd.read_file('../shapefiles/geo_export_9ef76f60-e019-451c-be6b-5a879a5e7c07.shp')
state_map = state_map.to_crs(epsg=2163)

district_map = gpd.read_file('../shapefiles/AgD Corn belt.shp')
district_map = district_map.to_crs(epsg=2163)
district = list(district_map['STASD_N'])


## Yield 
# Corn Grain values 
C_yield = df_geo_corn.loc[:,1998:2013].values  #kg/ha
Corn_emission= df_geo_corn_GHG.loc[:,1998:2013].values  #gCO2/MJ
Corn_cost= df_geo_corn_MFSP.loc[:,1998:2013].values  #$/MJ

# Soybean values
S_yield = df_geo_soy.loc[:,1998:2013].values  #kg/ha
Soy_emission = df_geo_soy_GHG.loc[:,1998:2013].values  #gCO2/MJ
Soy_cost = df_geo_soy_MFSP.loc[:,1998:2013].values    #$/MJ

# Grass values for marginal lands 
G_yield_AG = df_geo_grass_AG.loc[:,1998:2013].values  #yield in kg/ha
Grass_emission_AG = df_geo_grass_AG_GHG.loc[:,1998:2013].values  #gCO2/MJ
Grass_cost_AG = df_geo_grass_AG_MFSP.loc[:,1998:2013].values    #$/MJ

# Grass yield
G_yield_ML = df_geo_grass_ML.loc[:,1998:2013].values  #yield in kg/ha
Grass_emission_ML = df_geo_grass_ML_GHG.loc[:,1998:2013].values  #gCO2/MJ
Grass_cost_ML = df_geo_grass_ML_MFSP.loc[:,1998:2013].values    #$/MJ

# Algae yield
A_yield_AG = df_geo_algae_AG.loc[:,1998:2013].values  #yield in kg/ha
Algae_emission_AG = df_geo_algae_AG_GHG.loc[:,1998:2013].values  #gCO2/MJ
Algae_cost_AG = df_geo_algae_AG_MFSP.loc[:,1998:2013].values    #$/MJ

# Algae yield
A_yield_ML = df_geo_algae_ML.loc[:,1998:2013].values  #yield in kg/ha
Algae_emission_ML = df_geo_algae_ML_GHG.loc[:,1998:2013].values  #gCO2/MJ
Algae_cost_ML = df_geo_algae_ML_MFSP.loc[:,1998:2013].values    #$/MJ

## Land cost and limits 
land_limits = df_geo_corn.loc[:,'land_limits_ha'].values
marginal_land_limits_grass = df_geo_grass_ML.loc[:,'land_limits_ha'].values
marginal_land_limits_algae = df_geo_algae_ML.loc[:,'land_limits_ha'].values




#Mean Yield Calculation
total_yield_c = np.zeros((len(district))) # creating empty list for 106 total yield data set 
dist_mean_c = np.zeros((len(district))) # creating empty list for 106 mean yield data set 
total_yield_s = np.zeros((len(district))) # creating empty list for 106 total yield data set 
dist_mean_s = np.zeros((len(district))) # creating empty list for 106 mean yield data set 
total_yield_g = np.zeros((len(district))) # creating empty list for 106 total yield data set 
dist_mean_g = np.zeros((len(district))) # creating empty list for 106 mean yield data set
total_yield_a = np.zeros((len(district))) # creating empty list for 106 total yield data set 
dist_mean_a = np.zeros((len(district))) # creating empty list for 106 mean yield data set

total_en_c = np.zeros((len(district))) # creating empty list for 106 total yield data set 
dist_mean_en_c = np.zeros((len(district))) # creating empty list for 106 mean yield data set 
total_en_s = np.zeros((len(district))) # creating empty list for 106 total yield data set 
dist_mean_en_s = np.zeros((len(district))) # creating empty list for 106 mean yield data set 
total_en_g = np.zeros((len(district))) # creating empty list for 106 total yield data set 
dist_mean_en_g = np.zeros((len(district))) # creating empty list for 106 mean yield data set
total_en_a = np.zeros((len(district))) # creating empty list for 106 total yield data set 
dist_mean_en_a = np.zeros((len(district))) # creating empty list for 106 mean yield data set

total_MFSP_c = np.zeros((len(district))) # creating empty list for 106 total yield data set 
dist_mean_MFSP_c = np.zeros((len(district))) # creating empty list for 106 mean yield data set 
total_MFSP_s = np.zeros((len(district))) # creating empty list for 106 total yield data set 
dist_mean_MFSP_s = np.zeros((len(district))) # creating empty list for 106 mean yield data set 
total_MFSP_g = np.zeros((len(district))) # creating empty list for 106 total yield data set 
dist_mean_MFSP_g = np.zeros((len(district))) # creating empty list for 106 mean yield data set
total_MFSP_a = np.zeros((len(district))) # creating empty list for 106 total yield data set 
dist_mean_MFSP_a = np.zeros((len(district))) # creating empty list for 106 mean yield data set

for dist in district:
    i = district.index(dist) #for selecting specific district, for loop created and each district index founded 
    C = sum(C_yield[i,:]) # for each district summation of total yield throughout 63 years founded
    total_yield_c[i] = C # set all total yield value into created list 
    mean_yield = C/(len(years)) #calculating mean yield for each district by dividing year length
    dist_mean_c[i] = mean_yield  # set all mean yield value into created list 
    
    
    C_MFSP = sum(Corn_cost[i,:])
    total_MFSP_c[i] = C_MFSP 
    mean_energy = C_MFSP/(len(years))
    dist_mean_MFSP_c[i] = mean_energy

for dist in district:
    i = district.index(dist) #for selecting specific district, for loop created and each district index founded 
    S = sum(S_yield[i,:]) # for each district summation of total yield throughout 63 years founded
    total_yield_s[i] = S # set all total yield value into created list 
    mean_yield = S/(len(years)) #calculating mean yield for each district by dividing year length
    dist_mean_s[i] = mean_yield  # set all mean yield value into created list 

    
    S_MFSP = sum(Soy_cost[i,:])
    total_MFSP_s[i] = S_MFSP 
    mean_energy = S_MFSP/(len(years))
    dist_mean_MFSP_s[i] = mean_energy
    
for dist in district:
    i = district.index(dist) #for selecting specific district, for loop created and each district index founded 
    G = sum(G_yield_AG[i,:]) # for each district summation of total yield throughout 63 years founded
    total_yield_g[i] = G # set all total yield value into created list 
    mean_yield = G/(len(years)) #calculating mean yield for each district by dividing year length
    dist_mean_g[i] = mean_yield  # set all mean yield value into created list 

    
    G_MFSP = sum(Grass_cost_ML[i,:])
    total_MFSP_g[i] = G_MFSP 
    mean_energy = G_MFSP/(len(years))
    dist_mean_MFSP_g[i] = mean_energy
    
for dist in district:
    i = district.index(dist) #for selecting specific district, for loop created and each district index founded 
    A = sum(A_yield_AG[i,:]) # for each district summation of total yield throughout 63 years founded
    total_yield_a[i] = A # set all total yield value into created list 
    mean_yield = A/(len(years)) #calculating mean yield for each district by dividing year length
    dist_mean_a[i] = mean_yield  # set all mean yield value into created list 

    
    A_MFSP = sum(Algae_cost_ML[i,:])
    total_MFSP_a[i] = A_MFSP 
    mean_energy = A_MFSP/(len(years))
    dist_mean_MFSP_a[i] = mean_energy

## OPTIONS
# tc = dist_mean_c
# tc = dist_mean_s
# tc = dist_mean_g
# tc = dist_mean_a
# tc = land_cost
# tc = land_limits
# tc = marginal_LC
# tc = marginal_land_limits
# tc = electricity
# tc = dist_mean_en_c
# tc = dist_mean_en_s
# tc = dist_mean_en_g
# tc = dist_mean_en_a
# tc = dist_mean_MFSP_c
# tc = dist_mean_MFSP_s
# tc = dist_mean_MFSP_g
tc = dist_mean_MFSP_a


t = tc
to = t  # .iloc[1:]



# district_map.index = to.index
map_c = pd.concat([district_map],axis=1)
map_c['to'] = to

db = gpd.GeoDataFrame(map_c)
db.info()



f, ax = plt.subplots(1, figsize=(9, 9))

state_map.plot(ax=ax,color='gray',alpha=0.6,edgecolor='black',linewidth=0.8)


db.plot(column= to, 
        cmap= 'cool',
        edgecolor='black', 
        linewidth=0.8, 
        alpha=0.95, 
        legend=True,
        ax=ax
        )

# contextily.add_basemap(ax, 
#                         crs=db.crs, 
#                         source=contextily.providers.Stamen.TerrainBackground
#                       )
ax.set_axis_off()
ax.set_box_aspect(1)
ax.set_xlim(-750000,2000000)
ax.set_ylim([-2000000,500000])
plt.rcParams.update({'font.size': 10})

plt.rcParams['font.sans-serif'] = "Arial"
plt.axis('off')

print(min(tc))
print(max(tc))
#plt.savefig('max_energy_shortfall_c.tiff',dpi=300)   # idx1
#plt.savefig('min_GHG_emission_a.tiff',dpi=300)         # idx2
# plt.savefig('cost_c.tiff',dpi=300)                   # idx3 