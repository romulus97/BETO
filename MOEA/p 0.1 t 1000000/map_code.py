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

# #decision variables
# df_LC = pd.read_excel('Land cost.xlsx',header=0)
# df_D = df_LC.iloc[:,1:108]


df_decision_variables= pd.read_csv('Decision_Variables_borg_two_crop_trialdistrict.csv',header=0)
#tc = df_decision_variables.iloc[:,1:108]
#tc = df_decision_variables.iloc[:,108:215]
tc = df_decision_variables.iloc[:,215:]
t = tc.transpose(copy=False)
to = t  # .iloc[1:]
ind =  to.columns

district_map.index = to.index
map_c = pd.concat([district_map,to],axis=1)

db = gpd.GeoDataFrame(map_c)
db.info()

# l = list(df_O['min_energy_shortfall'])
i = 563

map_c = pd.concat([district_map,to],axis=1)

db = gpd.GeoDataFrame(map_c)
db.info()

f, ax = plt.subplots(1, figsize=(9, 9))
db.plot(column= i, 
        cmap='cool', 
        scheme='quantiles',
        k=5, 
        edgecolor='white', 
        linewidth=0., 
        alpha=0.75, 
        legend=True,
        legend_kwds={"loc": 2},
        ax=ax
        )
contextily.add_basemap(ax, 
                        crs=db.crs, 
                        source=contextily.providers.Stamen.TerrainBackground
                      )
ax.set_axis_off()
plt.axis('off')
#plt.savefig('min_energy_shortfall_rep_a.tiff',dpi=300)
#plt.savefig('energy_changes_c.tiff',dpi=300)
plt.savefig('cost_a.tiff',dpi=300)