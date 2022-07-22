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


df_geo_corn = pd.read_excel('combined_pivot_excel_electricity.xlsx',header=0, engine='openpyxl') #contains data sets for corn (state, land cost, yield etc)
df_geo_soy = pd.read_excel('combined_pivot_soy_excel_electricity.xlsx',header=0, engine='openpyxl') #contains data sets for soy (state, land cost, yield etc)
df_geo_grass = pd.read_excel('combined_pivot_grass_excel_electricity.xlsx',header=0, engine='openpyxl') #contains data sets for grass (state, land cost, yield etc) 
df_geo_algea = pd.read_excel('combined_pivot_algea_excel_electricity.xlsx',header=0, engine='openpyxl') #contains data sets for algae (state, land cost, yield etc)   

df = pd.read_csv('AgD_48g_cords_cb.csv',header=0)
years = range(1998,2014)
crs = {'init':'epsg:4326'}

geometry = [Point(xy) for xy in zip(df['Longitude'],df['Latitude'])]
geo_df = gpd.GeoDataFrame(df,crs=crs,geometry=geometry)
geo_df = geo_df.to_crs(epsg=2163)

state_map = gpd.read_file('shapefiles/geo_export_9ef76f60-e019-451c-be6b-5a879a5e7c07.shp')
state_map = state_map.to_crs(epsg=2163)

district_map = gpd.read_file('shapefiles/AgD Corn belt.shp')
district_map = district_map.to_crs(epsg=2163)
district = list(district_map['STASD_N'])

## Yield 
# Corn Grain yield
C_yield = df_geo_corn.loc[:,1998:2013].values  #yield in kg/ha

# Soybean yield
S_yield = df_geo_soy.loc[:,1998:2013].values  #yield in kg/ha

# Grass yield
G_yield = df_geo_grass.loc[:,1998:2013].values  #yield in kg/ha

# Algea yield
A_yield = df_geo_algea.loc[:,1998:2013].values  #yield in kg/ha


## Land cost and limits 
land_cost = df_geo_corn.loc[:,'land_costs-$/ha'].values # $ per ha
land_limits = df_geo_soy.loc[:,'land_limits_ha'].values
marginal_LC = df_geo_grass.loc[:,'land_costs-$/ha'].values # $ per ha
marginal_land_limits = df_geo_grass.loc[:,'land_limits_ha'].values
electricity = df_geo_corn.loc[:,'Electricity Price $/MJ'].values

#Mean Yield Calculation
total_yield_c = np.zeros((len(district))) # creating empty list for 106 total yield data set 
dist_mean_c = np.zeros((len(district))) # creating empty list for 106 mean yield data set 
total_yield_s = np.zeros((len(district))) # creating empty list for 106 total yield data set 
dist_mean_s = np.zeros((len(district))) # creating empty list for 106 mean yield data set 
total_yield_g = np.zeros((len(district))) # creating empty list for 106 total yield data set 
dist_mean_g = np.zeros((len(district))) # creating empty list for 106 mean yield data set
total_yield_a = np.zeros((len(district))) # creating empty list for 106 total yield data set 
dist_mean_a = np.zeros((len(district))) # creating empty list for 106 mean yield data set


for dist in district:
    i = district.index(dist) #for selecting specific district, for loop created and each district index founded 
    C = sum(C_yield[i,:]) # for each district summation of total yield throughout 63 years founded
    total_yield_c[i] = C # set all total yield value into created list 
    mean_yield = C/(len(years)) #calculating mean yield for each district by dividing year length
    dist_mean_c[i] = mean_yield  # set all mean yield value into created list 


for dist in district:
    i = district.index(dist) #for selecting specific district, for loop created and each district index founded 
    S = sum(S_yield[i,:]) # for each district summation of total yield throughout 63 years founded
    total_yield_s[i] = S # set all total yield value into created list 
    mean_yield = S/(len(years)) #calculating mean yield for each district by dividing year length
    dist_mean_s[i] = mean_yield  # set all mean yield value into created list 
    
for dist in district:
    i = district.index(dist) #for selecting specific district, for loop created and each district index founded 
    G = sum(G_yield[i,:]) # for each district summation of total yield throughout 63 years founded
    total_yield_g[i] = G # set all total yield value into created list 
    mean_yield = G/(len(years)) #calculating mean yield for each district by dividing year length
    dist_mean_g[i] = mean_yield  # set all mean yield value into created list 
    
for dist in district:
    i = district.index(dist) #for selecting specific district, for loop created and each district index founded 
    A = sum(A_yield[i,:]) # for each district summation of total yield throughout 63 years founded
    total_yield_a[i] = A # set all total yield value into created list 
    mean_yield = A/(len(years)) #calculating mean yield for each district by dividing year length
    dist_mean_a[i] = mean_yield  # set all mean yield value into created list 



df_decision_variables= pd.read_csv('Decision_Variables_borg_two_crop_trialdistrict.csv',header=0)

# tc = dist_mean_c
# tc = dist_mean_s
# tc = dist_mean_g
# tc = dist_mean_a
# tc = land_cost
# tc = land_limits
# tc = marginal_LC
# tc = marginal_land_limits
tc = electricity

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
        scheme='NaturalBreaks',
        k=15, 
        edgecolor='black', 
        linewidth=0.8, 
        alpha=0.95, 
        legend=False,
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
plt.axis('off')

#plt.savefig('max_energy_shortfall_c.tiff',dpi=300)   # idx1
#plt.savefig('min_GHG_emission_a.tiff',dpi=300)         # idx2
# plt.savefig('cost_c.tiff',dpi=300)                   # idx3 