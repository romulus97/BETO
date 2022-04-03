# -*- coding: utf-8 -*-
"""
Created on Wed Feb  2 11:57:07 2022

@author: Ece Ari Akdemir
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

df = pd.read_csv('AgD_48g_cords_cb.csv',header=0)
# cb_hubs = [4, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 36, 37, 44, 45, 46]
# for i in range(0,len(df)):
#     if df.loc[i,'Hubs'] in cb_hubs:
#         pass
#     else:
#         df.drop(i)

# df = df.reset_index(drop=True)

# crs=CRS('EPSG:4326')
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

fig,ax = plt.subplots()
state_map.plot(ax=ax,color='gray',alpha=0.6,edgecolor='white',linewidth=0.5)
district_map.plot(ax=ax,color='paleturquoise',alpha=1,edgecolor='black',linewidth=0.2)

ax.set_box_aspect(1)
ax.set_xlim(-750000,2000000)
ax.set_ylim([-2000000,500000])
plt.axis('off')
plt.savefig('districts.tiff',dpi=300)


#objective function
fn = 'Objective_Functions_borg_two_crop_trialdistrict.csv'
df_O = pd.read_csv(fn,header=0,index_col=0)
df_O.columns = ['cost','min_energy_shortfall','energy_changes']


df_decision_variables= pd.read_csv('Decision_Variables_borg_two_crop_trialdistrict.csv',header=0)
tc = df_decision_variables.iloc[:,0:108]
t = tc.transpose(copy=False)
to = t.iloc[1:]
ind =  to.columns

district_map.index = to.index
map_c = pd.concat([district_map,to],axis=1)

db = gpd.GeoDataFrame(map_c)
db.info()

Z1 = []

for i in ind:
    # f, ax = plt.subplots(1, figsize=(9, 9))
    # db.plot(column= i, 
    #         cmap='viridis', 
    #         scheme='quantiles',
    #         k=5, 
    #         edgecolor='white', 
    #         linewidth=0., 
    #         alpha=0.75, 
    #         legend=True,
    #         legend_kwds={"loc": 2},
    #         ax=ax
    #        )
    # contextily.add_basemap(ax, 
    #                        crs=db.crs, 
    #                        source=contextily.providers.Stamen.TerrainBackground
    #                       )
    # ax.set_axis_off()
    
    # Generate W from the GeoDataFrame
    w = weights.KNN.from_dataframe(db, k=8)
    # Row-standardization
    w.transform = 'R'
    
    w.transform = 'R'
    moran = esda.moran.Moran(db[i], w)
    moran.I
    Z1.append(moran.I)


# for i in ind:
#     Z = df_decision_variables.iloc[i-1:i,1:]
    
#     #Create the matrix of weigthts 
#     w = lat2W(Z.shape[0], Z.shape[1])
#     # Crate the pysal Moran object 
#     mi = Moran(Z, w)
#     # Verify Moran's I results 
#     Z1.append(mi.I)

Z2 = [x for x in Z1 if np.isnan(x) == False]
print(Z2)
Z3 = min(Z2)
idx1c = Z2.index(Z3)

Z4 = max(Z2)
idx1c_c = Z2.index(Z4)

######################### GRASS ########################

#moran for grass
tg = df_decision_variables.iloc[:,108:215]
tg1 = tg.transpose(copy=False)
indg =  tg1.columns

district_map.index = tg1.index
map_g = pd.concat([district_map,tg1],axis=1)

dbg = gpd.GeoDataFrame(map_g)
dbg.info()

Z1_g = []

for i in indg:
    
    # Generate W from the GeoDataFrame
    wg = weights.KNN.from_dataframe(dbg, k=8)
    # Row-standardization
    wg.transform = 'R'

    morang = esda.moran.Moran(dbg[i], wg)
    morang.I
    Z1_g.append(morang.I)


Z2g = [x for x in Z1_g if np.isnan(x) == False]
print(Z2g)
Z3g = min(Z2g)
idx1g = Z2g.index(Z3g)

Z4g = max(Z2g)
idx1g_c = Z2g.index(Z4g)

######################## ALGAE #####################

#moran for algae
ta = df_decision_variables.iloc[:,215:]
ta1 = ta.transpose(copy=False)
inda =  ta1.columns

district_map.index = ta1.index
map_a = pd.concat([district_map,ta1],axis=1)

dba = gpd.GeoDataFrame(map_a)
dba.info()

Z1_a = []

for i in inda:

    
    # Generate W from the GeoDataFrame
    wa = weights.KNN.from_dataframe(dba, k=8)
    # Row-standardization
    wa.transform = 'R'

    morana = esda.moran.Moran(dba[i], wa)
    morana.I
    Z1_a.append(morana.I)


Z2a = [x for x in Z1_a if np.isnan(x) == False]
print(Z2a)
Z3a = min(Z2a)
idx1a = Z2a.index(Z3a)

Z4a = max(Z2a)
idx1a_c = Z2a.index(Z4a)


######### COMBINED MORAN'S I #################

com_c = to.reset_index(drop=True)
com_g = tg1.reset_index(drop=True)
com_a = ta1.reset_index(drop=True)

comb = com_a.add(com_g)
com_b = comb.reset_index(drop=True)
com = com_c.add(com_b)

ind_com =  com.columns

district_map.index = com.index
map_com = pd.concat([district_map,com],axis=1)

db_com = gpd.GeoDataFrame(map_com)
db_com.info()

Z1_com = []

for i in ind_com:
    
    # Generate W from the GeoDataFrame
    wcom = weights.KNN.from_dataframe(db_com, k=8)
    # Row-standardization
    wcom.transform = 'R'

    moran_com = esda.moran.Moran(db_com[i], wcom)
    moran_com.I
    Z1_com.append(moran_com.I)


Z2_com = [x for x in Z1_com if np.isnan(x) == False]
print(Z2_com)
Z3_com = min(Z2_com)
idx1_com = Z2_com.index(Z3_com)

Z4_com = max(Z2_com)
idx1_com_c = Z2_com.index(Z4_com)


# df_O['Morans_I_cs'] = Z1

# seaborn.pairplot(df_O, hue ='Morans_I_cs', palette = 'rainbow')
# # to show
# plt.show()
# plt.savefig('Pair plot for Morans.tiff',dpi=300)



# df_O['Morans_I_g'] = Z1_g


# seaborn.pairplot(df_O, hue ='Morans_I_g', palette = 'rainbow')
# # to show
# plt.show()
# plt.savefig('Pair plot for Morans_grass.tiff')



df_O['Morans_I_a'] = Z1_a


seaborn.pairplot(df_O, hue ='Morans_I_a', palette = 'rainbow')
# to show
plt.show()
# plt.savefig('Pair plot for Morans_algae.tiff')




