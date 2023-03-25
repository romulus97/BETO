# -*- coding: utf-8 -*-
"""
Created on Fri Mar 11 10:53:37 2022

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



df = pd.read_csv('AgD_48g_cords_cb.csv',header=0)


crs = {'init':'epsg:4326'}
# crs = {"init": "epsg:2163"}
geometry = [Point(xy) for xy in zip(df['Longitude'],df['Latitude'])]
geo_df = gpd.GeoDataFrame(df,crs=crs,geometry=geometry)
geo_df = geo_df.to_crs(epsg=2163)

state_map = gpd.read_file('shapefiles/geo_export_9ef76f60-e019-451c-be6b-5a879a5e7c07.shp')
state_map = state_map.to_crs(epsg=2163)

district_map = gpd.read_file('shapefiles/AgD Corn belt.shp')
district_map = district_map.to_crs(epsg=2163)
districts = list(district_map['STASD_N'])

fig,ax = plt.subplots(1, figsize=(40, 20))
district_map.plot(ax=ax,color='gray',alpha=0.6,edgecolor='black',linewidth=0.8)


district_map['coords'] = district_map['geometry'].apply(lambda x: x.representative_point().coords[:])
district_map['coords'] = [coords[0] for coords in district_map['coords']]
for idx, row in district_map.iterrows():
    ax.annotate(text=row['STASD_N'], xy=row['coords'],
                  horizontalalignment='center')
    
