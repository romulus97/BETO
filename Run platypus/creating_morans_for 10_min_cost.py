# -*- coding: utf-8 -*-
"""
Created on Tue Jun 21 16:13:50 2022

@author: eari
"""

import seaborn as sns
import pandas as pd
from pysal.lib import weights
from pysal.explore import esda
from pysal.viz.splot.esda import moran_scatterplot, lisa_cluster, plot_local_autocorrelation
import geopandas as gpd
import numpy as np
import contextily as ctx
import matplotlib.pyplot as plt
from libpysal.weights import lat2W
from esda.moran import Moran
from random import randint
import plotly.graph_objects as go
import plotly.io as pio
pio.renderers.default='browser'
import plotly.express as px
import pyproj
import scipy.stats

import seaborn
from numpy.random import seed
from shapely.geometry import Point, Polygon

version = 'district'

#####################################################################
##########           IMPORT DATA           ##########################
#####################################################################

df = pd.read_csv('AgD_48g_cords_cb.csv',header=0)
df_decision_variables= pd.read_csv('Decision_Variables_borg_two_crop_trialdistrict.csv',header=0)
df_O = pd.read_csv('Objective_Functions_borg_two_crop_trialdistrict.csv',header=0,index_col=0)

crs = {'init':'epsg:4326'}

geometry = [Point(xy) for xy in zip(df['Longitude'],df['Latitude'])]
geo_df = gpd.GeoDataFrame(df,crs=crs,geometry=geometry)
geo_df = geo_df.to_crs(epsg=2163)

state_map = gpd.read_file('shapefiles/geo_export_9ef76f60-e019-451c-be6b-5a879a5e7c07.shp')
state_map = state_map.to_crs(epsg=2163)

district_map = gpd.read_file('shapefiles/AgD Corn belt.shp')
district_map = district_map.to_crs(epsg=2163)
districts = list(district_map['STASD_N'])

fig,ax = plt.subplots()
state_map.plot(ax=ax,color='gray',alpha=0.6,edgecolor='white',linewidth=0.5)
district_map.plot(ax=ax,color='paleturquoise',alpha=1,edgecolor='black',linewidth=0.2)

ax.set_box_aspect(1)
ax.set_xlim(-750000,2000000)
ax.set_ylim([-2000000,500000])
plt.axis('off')
plt.savefig('districts.tiff',dpi=300)


#objective function
# fn = 'Objective_Functions_borg_two_crop_trialdistrict.csv'
# df_O = pd.read_csv(fn,header=0,index_col=0)
df_O.columns = ['cost','max_energy_shortfall','min_GHG_emission']

# min cost solution 
sorting_cost = df_O.sort_values(by='cost', ascending=False)

min_10_cost = sorting_cost.tail(10)
ind_min_cost = list(min_10_cost.index.values)

Z1 = []

for ind in ind_min_cost:
    a = ind_min_cost.index(ind)

    tc = df_decision_variables.iloc[ind,1:108]
    tg = df_decision_variables.iloc[ind,108:215].reset_index(drop=True)
    # ttg = tg.reset_index().iloc[:,1]
    ta = df_decision_variables.iloc[ind,215:].reset_index(drop=True)
    # tta = ta.reset_index().iloc[:,1]
    tt = tc.values + tg.values + ta.values
    tts = pd.Series(tt)
    district_map.index =  tts.index
    map_c = pd.concat([district_map,tts],axis=1)
    
    db = gpd.GeoDataFrame(map_c)
    db.info()

    w = weights.KNN.from_dataframe(db, k=8)
    w.transform = 'R'
    
    w.transform = 'R'
    moran = esda.moran.Moran(db.iloc[:,4], w)
    moran.I
    Z1.append(moran.I)

# min shortfall solution 
sorting_shortfall = df_O.sort_values(by='max_energy_shortfall', ascending=False)

min_10_shortfall = sorting_shortfall.tail(10)
ind_min_shortfall = list(min_10_shortfall.index.values)

Z2 = []

for ind in ind_min_shortfall:
    a = ind_min_shortfall.index(ind)

    tc = df_decision_variables.iloc[ind,1:108]
    tg = df_decision_variables.iloc[ind,108:215].reset_index(drop=True)
    # ttg = tg.reset_index().iloc[:,1]
    ta = df_decision_variables.iloc[ind,215:].reset_index(drop=True)
    # tta = ta.reset_index().iloc[:,1]
    tt = tc.values + tg.values + ta.values
    tts = pd.Series(tt)
    district_map.index =  tts.index
    map_c = pd.concat([district_map,tts],axis=1)
    
    db = gpd.GeoDataFrame(map_c)
    db.info()

    w = weights.KNN.from_dataframe(db, k=8)
    w.transform = 'R'
    
    w.transform = 'R'
    moran = esda.moran.Moran(db.iloc[:,4], w)
    moran.I
    Z2.append(moran.I)


# min GHG solution 
sorting_GHG = df_O.sort_values(by='min_GHG_emission', ascending=False)

min_10_GHG = sorting_GHG.tail(10)
ind_min_GHG = list(min_10_GHG.index.values)

Z3 = []

for ind in ind_min_GHG:
    a = ind_min_GHG.index(ind)

    tc = df_decision_variables.iloc[ind,1:108]
    tg = df_decision_variables.iloc[ind,108:215].reset_index(drop=True)
    # ttg = tg.reset_index().iloc[:,1]
    ta = df_decision_variables.iloc[ind,215:].reset_index(drop=True)
    # tta = ta.reset_index().iloc[:,1]
    tt = tc.values + tg.values + ta.values
    tts = pd.Series(tt)
    district_map.index =  tts.index
    map_c = pd.concat([district_map,tts],axis=1)
    
    db = gpd.GeoDataFrame(map_c)
    db.info()

    w = weights.KNN.from_dataframe(db, k=8)
    w.transform = 'R'
    
    w.transform = 'R'
    moran = esda.moran.Moran(db.iloc[:,4], w)
    moran.I
    Z3.append(moran.I)
