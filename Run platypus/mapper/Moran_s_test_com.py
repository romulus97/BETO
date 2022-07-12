# -*- coding: utf-8 -*-
"""
Created on Sun Jan 30 18:33:15 2022

@author: Ece Ari Akdemir
"""


# import seaborn as sns
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
import numpy as np
from random import randint
import plotly.graph_objects as go
import plotly.io as pio
pio.renderers.default='browser'
import plotly.express as px
import plotly.express as px
import scipy.stats


import seaborn

import contextily
# Analysis
from numpy.random import seed

import matplotlib
from shapely.geometry import Point, Polygon

df = pd.read_csv('AgD_48g_cords_cb.csv',header=0)
# cb_hubs = [4, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 36, 37, 44, 45, 46]
# for i in range(0,len(df)):
#     if df.loc[i,'Hubs'] in cb_hubs:
#         pass
#     else:
#         df.drop(i)

# df = df.reset_index(drop=True)

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


#############################################################
##################### PLOTS #################################



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
import numpy as np
from random import randint


df_decision_variables= pd.read_csv('Decision_Variables_borg_two_crop_trialdistrict.csv',header=0) 

# idx1c = 1346
# idx1g = 137
# idx1a = 69

# idx1_com = 549

# idx1c_c = 1109
# idx1g_c = 1564
# idx1a_c = 1345

# idx1_com_c = 1354

version = 'district'

import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import geopandas as gpd
from shapely.geometry import Point, Polygon


df = pd.read_csv('AgD_48g_cords_cb.csv',header=0)
# cb_hubs = [4, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 36, 37, 44, 45, 46]
# for i in range(0,len(df)):
#     if df.loc[i,'Hubs'] in cb_hubs:
#         pass
#     else:
#         df.drop(i)

# df = df.reset_index(drop=True)

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

fig,ax = plt.subplots()
state_map.plot(ax=ax,color='gray',alpha=0.6,edgecolor='white',linewidth=0.5)
# cb_counties.plot(ax=ax,color='orange',alpha=1,edgecolor='darkslategrey',linewidth=0.2)   
district_map.plot(ax=ax,color='paleturquoise',alpha=1,edgecolor='black',linewidth=0.5)

#selected hubs
geo_df.plot(ax=ax,markersize=16,color='red',marker='o',edgecolor='white',linewidth=1)

ax.set_box_aspect(1)
ax.set_xlim(-750000,2000000)
ax.set_ylim([-2000000,500000])
plt.axis('off') 

plt.savefig('hubs.tiff',dpi=300)


#objective function
fn = 'Objective_Functions_borg_two_crop_trial' + version + '.csv'
df_O = pd.read_csv(fn,header=0,index_col=0)
df_O.columns = ['cost','min_energy_shortfall','energy_changes']

r = []
t = []
l = []
nd = []

# R = 100000000000000000
# T = 100000000000000000
# L = 100000000000000000

for i in range(0,len(df_O)):
    if i < 1:
        r.append(df_O.loc[i,'min_energy_shortfall']/(10**9))
        t.append(df_O.loc[i,'energy_changes']/(10**11))
        l.append(df_O.loc[i,'cost']/(10**13))
        nd.append(i)
    else:
        n = 1
        for j in r:
            idx = r.index(j)
            if r[idx] < df_O.loc[i,'min_energy_shortfall']/(10**9) and t[idx] < df_O.loc[i,'energy_changes']/(10**11) and l[idx] < df_O.loc[i,'cost']/(10**13):
                n = 0
        if n > 0:
            r.append(df_O.loc[i,'min_energy_shortfall']/(10**9))
            t.append(df_O.loc[i,'energy_changes']/(10**11))   
            l.append(df_O.loc[i,'cost']/(10**13)) 
            nd.append(idx)
    for k in r:
        idx = r.index(k)
        if r[0] > r[idx] and t[0] > t[idx] and l[0] > l[idx]:
            r.pop(0)
            t.pop(0)
            l.pop(0)
            
span = max(l) - min(l)

for i in range(0,len(l)):
    l[i] = 2*(l[i] - min(l))/span


fig = plt.figure()
ax = fig.add_subplot(projection='3d')

p = ax.scatter(r,t,l, c=r, s=l, cmap='hot',linewidth=1, edgecolor='black')
# fig.colorbar(p, ax=ax)
fig.colorbar(p, ax=ax, location='left', shrink=0.6)
# ax.scatter(r,t,l,)

# plt.figure()
# plt.scatter(r,t)
ax.set_xlabel('min_energy_shortfall',fontweight='bold', fontsize=10)
ax.set_ylabel('energy_changes',fontweight='bold',fontsize=10)
ax.set_zlabel('cost',fontweight='bold',fontsize=10)

plt.savefig('pareto.tiff',dpi = 330)
    
    
#decision variables
fn = 'Decision_Variables_borg_two_crop_trial' + version + '.csv'
df_DE = pd.read_csv(fn,header=0,index_col=0)
df_D = df_DE.iloc[:,0:107]

df_G = df_DE.iloc[:,107:214]

df_A = df_DE.iloc[:,214:]



######################## CORN ############################

l = list(df_O['min_energy_shortfall'])
# idx1 = l.index(min(l))

d_sample = list(df_D.iloc[idx1c,0:len(districts)])
cmap = matplotlib.cm.get_cmap('cool')
# M = max(d_sample)
M = np.max(df_D.iloc[:,0:len(districts)].values)

# plt.savefig('min_ref_capex.tiff',dpi=300)
C = []
fractions = []
sample_Cs = []
for i in range(0,len(district_map)):
    f = float(district_map.loc[i,'STASD_N'])    
    idx = districts.index(f)
    if not idx:
        if idx < 1:
            d_value = d_sample[idx]
            fraction = d_value/M
            fractions.append(fraction)
            sample_c = cmap(fraction)
            sample_Cs.append(sample_c)
            hexa = matplotlib.colors.rgb2hex(sample_c)
            C.append(hexa)
        else:    
            fraction = 0/M
            fractions.append(fraction)
            sample_c = cmap(fraction)
            sample_Cs.append(sample_c)
            hexa = matplotlib.colors.rgb2hex(sample_c)
            C.append(hexa)
            # C.append(C[-1])
    else:
        d_value = d_sample[idx]
        fraction = d_value/M
        fractions.append(fraction)
        sample_c = cmap(fraction)
        sample_Cs.append(sample_c)
        hexa = matplotlib.colors.rgb2hex(sample_c)
        C.append(hexa)
        
district_map['color'] = C

d_sample = list(df_D.iloc[idx1c,len(districts):])
dvs = int(np.sqrt(len(d_sample)))
refinery_flow = np.zeros((dvs,))
for i in range(0,dvs):
    for j in range(0,dvs):
        f = d_sample[i*dvs+j]
        refinery_flow[j] += f

# mx = np.max(df_D.iloc[:,len(districts):].values)

# for i in range(0,dvs):
#     refinery_flow[i] = (refinery_flow[i]/mx)*16

# geo_df['marker_size'] = refinery_flow

fig,ax = plt.subplots()

state_map.plot(ax=ax,color='gray',alpha=0.6,edgecolor='white',linewidth=0.5)
# district_map.plot(ax=ax,color='white',alpha=1,edgecolor='darkslategrey',linewidth=0.2)   
district_map.plot(ax=ax,color=list(district_map['color']),alpha=1,edgecolor='none',linewidth=0.8)

# plot refineries
# geo_df.plot(ax=ax,markersize=geo_df['marker_size'],color="None",marker='o',edgecolor='black',linewidth=1)
geo_df.plot(ax=ax,color="None",marker='o',edgecolor='black',linewidth=1)

ax.set_box_aspect(1)
ax.set_xlim(-750000,2000000)
ax.set_ylim([-2000000,500000])
plt.axis('off')

plt.savefig('dispersed_crop_area.tiff',dpi=300)




############################ GRASS ################################

# find sispersed land for grass 
#minimum land_costs
d_sample = list(df_G.iloc[idx1g,0:len(districts)])
cmap = matplotlib.cm.get_cmap('cool')
# M = max(d_sample)
M = np.max(df_G.iloc[:,0:len(districts)].values)

# plt.savefig('min_ref_capex.tiff',dpi=300)
C = []
fractions = []
sample_Cs = []
for i in range(0,len(district_map)):
    f = float(district_map.loc[i,'STASD_N'])    
    idx = districts.index(f)
    if not idx:
        if idx < 1:
            d_value = d_sample[idx]
            fraction = d_value/M
            fractions.append(fraction)
            sample_c = cmap(fraction)
            sample_Cs.append(sample_c)
            hexa = matplotlib.colors.rgb2hex(sample_c)
            C.append(hexa)
        else:    
            fraction = 0/M
            fractions.append(fraction)
            sample_c = cmap(fraction)
            sample_Cs.append(sample_c)
            hexa = matplotlib.colors.rgb2hex(sample_c)
            C.append(hexa)
    else:
        d_value = d_sample[idx]
        fraction = d_value/M
        fractions.append(fraction)
        sample_c = cmap(fraction)
        sample_Cs.append(sample_c)
        hexa = matplotlib.colors.rgb2hex(sample_c)
        C.append(hexa)
        
district_map['color'] = C

# d_sample = list(df_D.iloc[idx3,len(districts):])
# dvs = int(np.sqrt(len(d_sample)))
# refinery_flow = np.zeros((dvs,))
# for i in range(0,dvs):
#     for j in range(0,dvs):
#         f = d_sample[i*dvs+j]
#         refinery_flow[j] += f

# mx = np.max(df_D.iloc[:,len(districts):].values)

# for i in range(0,dvs):
#     refinery_flow[i] = (refinery_flow[i]/mx)*16

# geo_df['marker_size'] = refinery_flow

fig,ax = plt.subplots()

state_map.plot(ax=ax,color='gray',alpha=0.6,edgecolor='white',linewidth=0.5)
# district_map.plot(ax=ax,color='white',alpha=1,edgecolor='darkslategrey',linewidth=0.2)   
district_map.plot(ax=ax,color=list(district_map['color']),alpha=1,edgecolor='none',linewidth=0.8)

# plot refineries
# geo_df.plot(ax=ax,markersize=geo_df['marker_size'],color="None",marker='o',edgecolor='black',linewidth=1)
geo_df.plot(ax=ax,color="None",marker='o',edgecolor='black',linewidth=1)

ax.set_box_aspect(1)
ax.set_xlim(-750000,2000000)
ax.set_ylim([-2000000,500000])
plt.axis('off')

plt.savefig('dispersed_crop_land_grass.tiff',dpi=300)


########################################## ALGAE ###############################

#minimum capex for algea

#minimum land_costs
d_sample = list(df_A.iloc[idx1a,0:len(districts)])
cmap = matplotlib.cm.get_cmap('cool')
# M = max(d_sample)
M = np.max(df_A.iloc[:,0:len(districts)].values)

# plt.savefig('min_ref_capex.tiff',dpi=300)
C = []
fractions = []
sample_Cs = []
for i in range(0,len(district_map)):
    f = float(district_map.loc[i,'STASD_N'])    
    idx = districts.index(f)
    if not idx:
        if idx < 1:
            d_value = d_sample[idx]
            fraction = d_value/M
            fractions.append(fraction)
            sample_c = cmap(fraction)
            sample_Cs.append(sample_c)
            hexa = matplotlib.colors.rgb2hex(sample_c)
            C.append(hexa)
        else:    
            fraction = 0/M
            fractions.append(fraction)
            sample_c = cmap(fraction)
            sample_Cs.append(sample_c)
            hexa = matplotlib.colors.rgb2hex(sample_c)
            C.append(hexa)
    else:
        d_value = d_sample[idx]
        fraction = d_value/M
        fractions.append(fraction)
        sample_c = cmap(fraction)
        sample_Cs.append(sample_c)
        hexa = matplotlib.colors.rgb2hex(sample_c)
        C.append(hexa)
        
district_map['color'] = C

# d_sample = list(df_D.iloc[idx3,len(districts):])
# dvs = int(np.sqrt(len(d_sample)))
# refinery_flow = np.zeros((dvs,))
# for i in range(0,dvs):
#     for j in range(0,dvs):
#         f = d_sample[i*dvs+j]
#         refinery_flow[j] += f

# mx = np.max(df_D.iloc[:,len(districts):].values)

# for i in range(0,dvs):
#     refinery_flow[i] = (refinery_flow[i]/mx)*16

# geo_df['marker_size'] = refinery_flow

fig,ax = plt.subplots()

state_map.plot(ax=ax,color='gray',alpha=0.6,edgecolor='white',linewidth=0.5)
# district_map.plot(ax=ax,color='white',alpha=1,edgecolor='darkslategrey',linewidth=0.2)   
district_map.plot(ax=ax,color=list(district_map['color']),alpha=1,edgecolor='none',linewidth=0.8)

# plot refineries
# geo_df.plot(ax=ax,markersize=geo_df['marker_size'],color="None",marker='o',edgecolor='black',linewidth=1)
geo_df.plot(ax=ax,color="None",marker='o',edgecolor='black',linewidth=1)

ax.set_box_aspect(1)
ax.set_xlim(-750000,2000000)
ax.set_ylim([-2000000,500000])
plt.axis('off')

plt.savefig('dispersed_crop_land_algae.tiff',dpi=300)


########################### CLUSTERED ########################################
######################## CORN ############################

l = list(df_O['min_energy_shortfall'])
# idx1 = l.index(min(l))

d_sample = list(df_D.iloc[idx1c_c,0:len(districts)])
cmap = matplotlib.cm.get_cmap('cool')
# M = max(d_sample)
M = np.max(df_D.iloc[:,0:len(districts)].values)

# plt.savefig('min_ref_capex.tiff',dpi=300)
C = []
fractions = []
sample_Cs = []
for i in range(0,len(district_map)):
    f = float(district_map.loc[i,'STASD_N'])    
    idx = districts.index(f)
    if not idx:
        if idx < 1:
            d_value = d_sample[idx]
            fraction = d_value/M
            fractions.append(fraction)
            sample_c = cmap(fraction)
            sample_Cs.append(sample_c)
            hexa = matplotlib.colors.rgb2hex(sample_c)
            C.append(hexa)
        else:    
            fraction = 0/M
            fractions.append(fraction)
            sample_c = cmap(fraction)
            sample_Cs.append(sample_c)
            hexa = matplotlib.colors.rgb2hex(sample_c)
            C.append(hexa)
            # C.append(C[-1])
    else:
        d_value = d_sample[idx]
        fraction = d_value/M
        fractions.append(fraction)
        sample_c = cmap(fraction)
        sample_Cs.append(sample_c)
        hexa = matplotlib.colors.rgb2hex(sample_c)
        C.append(hexa)
        
district_map['color'] = C

d_sample = list(df_D.iloc[idx1c_c,len(districts):])
dvs = int(np.sqrt(len(d_sample)))
refinery_flow = np.zeros((dvs,))
for i in range(0,dvs):
    for j in range(0,dvs):
        f = d_sample[i*dvs+j]
        refinery_flow[j] += f

# mx = np.max(df_D.iloc[:,len(districts):].values)

# for i in range(0,dvs):
#     refinery_flow[i] = (refinery_flow[i]/mx)*16

# geo_df['marker_size'] = refinery_flow

fig,ax = plt.subplots()

state_map.plot(ax=ax,color='gray',alpha=0.6,edgecolor='white',linewidth=0.5)
# district_map.plot(ax=ax,color='white',alpha=1,edgecolor='darkslategrey',linewidth=0.2)   
district_map.plot(ax=ax,color=list(district_map['color']),alpha=1,edgecolor='none',linewidth=0.8)

# plot refineries
# geo_df.plot(ax=ax,markersize=geo_df['marker_size'],color="None",marker='o',edgecolor='black',linewidth=1)
geo_df.plot(ax=ax,color="None",marker='o',edgecolor='black',linewidth=1)

ax.set_box_aspect(1)
ax.set_xlim(-750000,2000000)
ax.set_ylim([-2000000,500000])
plt.axis('off')

plt.savefig('clustered_crop_area.tiff',dpi=300)




############################ GRASS ################################

# find sispersed land for grass 
#minimum land_costs
d_sample = list(df_G.iloc[idx1g_c,0:len(districts)])
cmap = matplotlib.cm.get_cmap('cool')
# M = max(d_sample)
M = np.max(df_G.iloc[:,0:len(districts)].values)

# plt.savefig('min_ref_capex.tiff',dpi=300)
C = []
fractions = []
sample_Cs = []
for i in range(0,len(district_map)):
    f = float(district_map.loc[i,'STASD_N'])    
    idx = districts.index(f)
    if not idx:
        if idx < 1:
            d_value = d_sample[idx]
            fraction = d_value/M
            fractions.append(fraction)
            sample_c = cmap(fraction)
            sample_Cs.append(sample_c)
            hexa = matplotlib.colors.rgb2hex(sample_c)
            C.append(hexa)
        else:    
            fraction = 0/M
            fractions.append(fraction)
            sample_c = cmap(fraction)
            sample_Cs.append(sample_c)
            hexa = matplotlib.colors.rgb2hex(sample_c)
            C.append(hexa)
    else:
        d_value = d_sample[idx]
        fraction = d_value/M
        fractions.append(fraction)
        sample_c = cmap(fraction)
        sample_Cs.append(sample_c)
        hexa = matplotlib.colors.rgb2hex(sample_c)
        C.append(hexa)
        
district_map['color'] = C

# d_sample = list(df_D.iloc[idx3,len(districts):])
# dvs = int(np.sqrt(len(d_sample)))
# refinery_flow = np.zeros((dvs,))
# for i in range(0,dvs):
#     for j in range(0,dvs):
#         f = d_sample[i*dvs+j]
#         refinery_flow[j] += f

# mx = np.max(df_D.iloc[:,len(districts):].values)

# for i in range(0,dvs):
#     refinery_flow[i] = (refinery_flow[i]/mx)*16

# geo_df['marker_size'] = refinery_flow

fig,ax = plt.subplots()

state_map.plot(ax=ax,color='gray',alpha=0.6,edgecolor='white',linewidth=0.5)
# district_map.plot(ax=ax,color='white',alpha=1,edgecolor='darkslategrey',linewidth=0.2)   
district_map.plot(ax=ax,color=list(district_map['color']),alpha=1,edgecolor='none',linewidth=0.8)

# plot refineries
# geo_df.plot(ax=ax,markersize=geo_df['marker_size'],color="None",marker='o',edgecolor='black',linewidth=1)
geo_df.plot(ax=ax,color="None",marker='o',edgecolor='black',linewidth=1)

ax.set_box_aspect(1)
ax.set_xlim(-750000,2000000)
ax.set_ylim([-2000000,500000])
plt.axis('off')

plt.savefig('clustered_crop_land_grass.tiff',dpi=300)


################################### ALGAE ####################################

#minimum capex for algea

#minimum land_costs
d_sample = list(df_A.iloc[idx1a_c,0:len(districts)])
cmap = matplotlib.cm.get_cmap('cool')
# M = max(d_sample)
M = np.max(df_A.iloc[:,0:len(districts)].values)

# plt.savefig('min_ref_capex.tiff',dpi=300)
C = []
fractions = []
sample_Cs = []
for i in range(0,len(district_map)):
    f = float(district_map.loc[i,'STASD_N'])    
    idx = districts.index(f)
    if not idx:
        if idx < 1:
            d_value = d_sample[idx]
            fraction = d_value/M
            fractions.append(fraction)
            sample_c = cmap(fraction)
            sample_Cs.append(sample_c)
            hexa = matplotlib.colors.rgb2hex(sample_c)
            C.append(hexa)
        else:    
            fraction = 0/M
            fractions.append(fraction)
            sample_c = cmap(fraction)
            sample_Cs.append(sample_c)
            hexa = matplotlib.colors.rgb2hex(sample_c)
            C.append(hexa)
    else:
        d_value = d_sample[idx]
        fraction = d_value/M
        fractions.append(fraction)
        sample_c = cmap(fraction)
        sample_Cs.append(sample_c)
        hexa = matplotlib.colors.rgb2hex(sample_c)
        C.append(hexa)
        
district_map['color'] = C

# d_sample = list(df_D.iloc[idx3,len(districts):])
# dvs = int(np.sqrt(len(d_sample)))
# refinery_flow = np.zeros((dvs,))
# for i in range(0,dvs):
#     for j in range(0,dvs):
#         f = d_sample[i*dvs+j]
#         refinery_flow[j] += f

# mx = np.max(df_D.iloc[:,len(districts):].values)

# for i in range(0,dvs):
#     refinery_flow[i] = (refinery_flow[i]/mx)*16

# geo_df['marker_size'] = refinery_flow

fig,ax = plt.subplots()

state_map.plot(ax=ax,color='gray',alpha=0.6,edgecolor='white',linewidth=0.5)
# district_map.plot(ax=ax,color='white',alpha=1,edgecolor='darkslategrey',linewidth=0.2)   
district_map.plot(ax=ax,color=list(district_map['color']),alpha=1,edgecolor='none',linewidth=0.8)

# plot refineries
# geo_df.plot(ax=ax,markersize=geo_df['marker_size'],color="None",marker='o',edgecolor='black',linewidth=1)
geo_df.plot(ax=ax,color="None",marker='o',edgecolor='black',linewidth=1)

ax.set_box_aspect(1)
ax.set_xlim(-750000,2000000)
ax.set_ylim([-2000000,500000])
plt.axis('off')

plt.savefig('clustered_crop_land_algae.tiff',dpi=300)


################################### COMBINED MAP  ####################################



######## DISPERSED ##############################


df_com = com.transpose(copy=False)

d_sample = list(df_com.iloc[idx1_com,0:len(districts)])
cmap = matplotlib.cm.get_cmap('cool')
# M = max(d_sample)
M = np.max(df_com.iloc[:,0:len(districts)].values)

# plt.savefig('min_ref_capex.tiff',dpi=300)
C = []
fractions = []
sample_Cs = []
for i in range(0,len(district_map)):
    f = float(district_map.loc[i,'STASD_N'])    
    idx = districts.index(f)
    if not idx:
        if idx < 1:
            d_value = d_sample[idx]
            fraction = d_value/M
            fractions.append(fraction)
            sample_c = cmap(fraction)
            sample_Cs.append(sample_c)
            hexa = matplotlib.colors.rgb2hex(sample_c)
            C.append(hexa)
        else:    
            fraction = 0/M
            fractions.append(fraction)
            sample_c = cmap(fraction)
            sample_Cs.append(sample_c)
            hexa = matplotlib.colors.rgb2hex(sample_c)
            C.append(hexa)
    else:
        d_value = d_sample[idx]
        fraction = d_value/M
        fractions.append(fraction)
        sample_c = cmap(fraction)
        sample_Cs.append(sample_c)
        hexa = matplotlib.colors.rgb2hex(sample_c)
        C.append(hexa)
        
district_map['color'] = C

# d_sample = list(df_D.iloc[idx3,len(districts):])
# dvs = int(np.sqrt(len(d_sample)))
# refinery_flow = np.zeros((dvs,))
# for i in range(0,dvs):
#     for j in range(0,dvs):
#         f = d_sample[i*dvs+j]
#         refinery_flow[j] += f

# mx = np.max(df_D.iloc[:,len(districts):].values)

# for i in range(0,dvs):
#     refinery_flow[i] = (refinery_flow[i]/mx)*16

# geo_df['marker_size'] = refinery_flow

fig,ax = plt.subplots()

state_map.plot(ax=ax,color='gray',alpha=0.6,edgecolor='white',linewidth=0.5)
# district_map.plot(ax=ax,color='white',alpha=1,edgecolor='darkslategrey',linewidth=0.2)   
district_map.plot(ax=ax,color=list(district_map['color']),alpha=1,edgecolor='none',linewidth=0.8)

# plot refineries
# geo_df.plot(ax=ax,markersize=geo_df['marker_size'],color="None",marker='o',edgecolor='black',linewidth=1)
geo_df.plot(ax=ax,color="None",marker='o',edgecolor='black',linewidth=1)

ax.set_box_aspect(1)
ax.set_xlim(-750000,2000000)
ax.set_ylim([-2000000,500000])
plt.axis('off')

plt.savefig('dispersed_crop_land_combined.tiff',dpi=300)


##### CLUSTERED ########################


d_sample = list(df_com.iloc[idx1_com_c,0:len(districts)])
cmap = matplotlib.cm.get_cmap('cool')
# M = max(d_sample)
M = np.max(df_com.iloc[:,0:len(districts)].values)

# plt.savefig('min_ref_capex.tiff',dpi=300)
C = []
fractions = []
sample_Cs = []
for i in range(0,len(district_map)):
    f = float(district_map.loc[i,'STASD_N'])    
    idx = districts.index(f)
    if not idx:
        if idx < 1:
            d_value = d_sample[idx]
            fraction = d_value/M
            fractions.append(fraction)
            sample_c = cmap(fraction)
            sample_Cs.append(sample_c)
            hexa = matplotlib.colors.rgb2hex(sample_c)
            C.append(hexa)
        else:    
            fraction = 0/M
            fractions.append(fraction)
            sample_c = cmap(fraction)
            sample_Cs.append(sample_c)
            hexa = matplotlib.colors.rgb2hex(sample_c)
            C.append(hexa)
    else:
        d_value = d_sample[idx]
        fraction = d_value/M
        fractions.append(fraction)
        sample_c = cmap(fraction)
        sample_Cs.append(sample_c)
        hexa = matplotlib.colors.rgb2hex(sample_c)
        C.append(hexa)
        
district_map['color'] = C

# d_sample = list(df_D.iloc[idx3,len(districts):])
# dvs = int(np.sqrt(len(d_sample)))
# refinery_flow = np.zeros((dvs,))
# for i in range(0,dvs):
#     for j in range(0,dvs):
#         f = d_sample[i*dvs+j]
#         refinery_flow[j] += f

# mx = np.max(df_D.iloc[:,len(districts):].values)

# for i in range(0,dvs):
#     refinery_flow[i] = (refinery_flow[i]/mx)*16

# geo_df['marker_size'] = refinery_flow

fig,ax = plt.subplots()

state_map.plot(ax=ax,color='gray',alpha=0.6,edgecolor='white',linewidth=0.5)
# district_map.plot(ax=ax,color='white',alpha=1,edgecolor='darkslategrey',linewidth=0.2)   
district_map.plot(ax=ax,color=list(district_map['color']),alpha=1,edgecolor='none',linewidth=0.8)

# plot refineries
# geo_df.plot(ax=ax,markersize=geo_df['marker_size'],color="None",marker='o',edgecolor='black',linewidth=1)
geo_df.plot(ax=ax,color="None",marker='o',edgecolor='black',linewidth=1)

ax.set_box_aspect(1)
ax.set_xlim(-750000,2000000)
ax.set_ylim([-2000000,500000])
plt.axis('off')

plt.savefig('clustered_crop_land_combined.tiff',dpi=300)





























