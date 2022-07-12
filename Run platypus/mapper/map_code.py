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


#######
class nlcmap(object):
    def __init__(self, cmap, levels):
        self.cmap = cmap
        self.N = cmap.N
        self.monochrome = self.cmap.monochrome
        self.levels = np.asarray(levels, dtype='float64')
        self._x = self.levels
        self.levmax = self.levels.max()
        self.transformed_levels = np.linspace(0.0, self.levmax,
              len(self.levels))

    def __call__(self, xi, alpha=1.0, **kw):
        yi = np.interp(xi, self._x, self.transformed_levels)
        return self.cmap(yi / self.levmax, alpha)


levels = [0, 4000, 6000, 8000, 10000, 12000, 14000, 16000, 18000, 100000, 230000]

cmap_nonlin = nlcmap(plt.cm.RdBu_r, levels)






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
tc = df_decision_variables.iloc[:,1:108]
#tc = df_decision_variables.iloc[:,108:215]
#tc = df_decision_variables.iloc[:,215:]
t = tc.transpose(copy=False)
to = t  # .iloc[1:]
ind =  to.columns

tt = df_decision_variables.iloc[:,1:108]
ttm = tt.loc[5531,:]

district_map.index = to.index
map_c = pd.concat([district_map,to],axis=1)

db = gpd.GeoDataFrame(map_c)
db.info()

## max energy shortfall 
#i = 54
## min_GHG_emission
#i = 7758
## min_cost
i = 7368

map_c = pd.concat([district_map,to],axis=1)


db = gpd.GeoDataFrame(map_c)
db.info()

f, ax = plt.subplots(1, figsize=(9, 9))

state_map.plot(ax=ax,color='gray',alpha=0.6,edgecolor='black',linewidth=0.8)


db.plot(column= i, 
        cmap= 'cool', 
        scheme='NaturalBreaks',
        k=15, 
        edgecolor='black', 
        linewidth=0.8, 
        alpha=0.95, 
        legend=True,
        legend_kwds={"loc": 4},
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
plt.savefig('cost_c.tiff',dpi=300)                   # idx3 