# -*- coding: utf-8 -*-
"""
Created on Tue Mar 30 12:57:35 2021
@author: jkern
"""
# -*- coding: utf-8 -*-
"""
Spyder Editor
This is a temporary script file.
"""

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
fn = 'Objective_Functions_' + version + '.csv'
df_O = pd.read_csv(fn,header=0,index_col=0)
df_O.columns = ['land','ref_capex','trans_opex']

r = []
t = []
l = []
nd = []

# R = 100000000000000000
# T = 100000000000000000
# L = 100000000000000000

for i in range(0,len(df_O)):
    if i < 1:
        r.append(df_O.loc[i,'ref_capex']/1000000000)
        t.append(df_O.loc[i,'trans_opex']/1000000000)
        l.append(df_O.loc[i,'land']/1000000)
        nd.append(i)
    else:
        n = 1
        for j in r:
            idx = r.index(j)
            if r[idx] < df_O.loc[i,'ref_capex']/1000000000 and t[idx] < df_O.loc[i,'trans_opex']/1000000000 and l[idx] < df_O.loc[i,'land']/1000000000:
                n = 0
        if n > 0:
            r.append(df_O.loc[i,'ref_capex']/1000000000)
            t.append(df_O.loc[i,'trans_opex']/1000000000)   
            l.append(df_O.loc[i,'land']/1000000) 
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
fig.colorbar(p, ax=ax)
# ax.scatter(r,t,l,)

# plt.figure()
# plt.scatter(r,t)
# plt.xlabel('Biofinery Capex $B',fontweight='bold',fontsize=12)
# plt.ylabel('Transporation Opex $B',fontweight='bold',fontsize=12)

plt.savefig('pareto.tiff',dpi = 330)
    
    
#decision variables
fn = 'Decision_Variables_' + version + '.csv'
df_D = pd.read_csv(fn,header=0,index_col=0)


#minimum capex

# find minimum capex

l = list(df_O['ref_capex'])
idx1 = l.index(min(l))

d_sample = list(df_D.iloc[idx1,0:len(districts)])
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

d_sample = list(df_D.iloc[idx1,len(districts):])
dvs = int(np.sqrt(len(d_sample)))
refinery_flow = np.zeros((dvs,))
for i in range(0,dvs):
    for j in range(0,dvs):
        f = d_sample[i*dvs+j]
        refinery_flow[j] += f

mx = np.max(df_D.iloc[:,len(districts):].values)

for i in range(0,dvs):
    refinery_flow[i] = (refinery_flow[i]/mx)*16

geo_df['marker_size'] = refinery_flow

fig,ax = plt.subplots()

state_map.plot(ax=ax,color='gray',alpha=0.6,edgecolor='white',linewidth=0.5)
# district_map.plot(ax=ax,color='white',alpha=1,edgecolor='darkslategrey',linewidth=0.2)   
district_map.plot(ax=ax,color=list(district_map['color']),alpha=1,edgecolor='none',linewidth=0.8)

# plot refineries
geo_df.plot(ax=ax,markersize=geo_df['marker_size'],color="None",marker='o',edgecolor='black',linewidth=1)


ax.set_box_aspect(1)
ax.set_xlim(-750000,2000000)
ax.set_ylim([-2000000,500000])
plt.axis('off')

plt.savefig('min_ref_cap.tiff',dpi=300)

# find minimum trans opex
l = list(df_O['trans_opex'])
idx2 = l.index(min(l))

#minimum trans opex
d_sample = list(df_D.iloc[idx2,0:len(districts)])
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
    else:
        d_value = d_sample[idx]
        fraction = d_value/M
        fractions.append(fraction)
        sample_c = cmap(fraction)
        sample_Cs.append(sample_c)
        hexa = matplotlib.colors.rgb2hex(sample_c)
        C.append(hexa)
        
district_map['color'] = C

d_sample = list(df_D.iloc[idx2,len(districts):])
dvs = int(np.sqrt(len(d_sample)))
refinery_flow = np.zeros((dvs,))
for i in range(0,dvs):
    for j in range(0,dvs):
        f = d_sample[i*dvs+j]
        refinery_flow[j] += f

mx = np.max(df_D.iloc[:,len(districts):].values)

for i in range(0,dvs):
    refinery_flow[i] = (refinery_flow[i]/mx)*16

geo_df['marker_size'] = refinery_flow

fig,ax = plt.subplots()

state_map.plot(ax=ax,color='gray',alpha=0.6,edgecolor='white',linewidth=0.5)
# district_map.plot(ax=ax,color='white',alpha=1,edgecolor='darkslategrey',linewidth=0.2)   
district_map.plot(ax=ax,color=list(district_map['color']),alpha=1,edgecolor='none',linewidth=0.8)

# plot refineries
geo_df.plot(ax=ax,markersize=geo_df['marker_size'],color="None",marker='o',edgecolor='black',linewidth=1)


ax.set_box_aspect(1)
ax.set_xlim(-750000,2000000)
ax.set_ylim([-2000000,500000])
plt.axis('off')

plt.savefig('min_trans_opex.tiff',dpi=300)


# find minimum land costs
l = list(df_O['land'])
idx3 = l.index(min(l))

#minimum land_costs
d_sample = list(df_D.iloc[idx3,0:len(districts)])
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
    else:
        d_value = d_sample[idx]
        fraction = d_value/M
        fractions.append(fraction)
        sample_c = cmap(fraction)
        sample_Cs.append(sample_c)
        hexa = matplotlib.colors.rgb2hex(sample_c)
        C.append(hexa)
        
district_map['color'] = C

d_sample = list(df_D.iloc[idx3,len(districts):])
dvs = int(np.sqrt(len(d_sample)))
refinery_flow = np.zeros((dvs,))
for i in range(0,dvs):
    for j in range(0,dvs):
        f = d_sample[i*dvs+j]
        refinery_flow[j] += f

mx = np.max(df_D.iloc[:,len(districts):].values)

for i in range(0,dvs):
    refinery_flow[i] = (refinery_flow[i]/mx)*16

geo_df['marker_size'] = refinery_flow

fig,ax = plt.subplots()

state_map.plot(ax=ax,color='gray',alpha=0.6,edgecolor='white',linewidth=0.5)
# district_map.plot(ax=ax,color='white',alpha=1,edgecolor='darkslategrey',linewidth=0.2)   
district_map.plot(ax=ax,color=list(district_map['color']),alpha=1,edgecolor='none',linewidth=0.8)

# plot refineries
geo_df.plot(ax=ax,markersize=geo_df['marker_size'],color="None",marker='o',edgecolor='black',linewidth=1)


ax.set_box_aspect(1)
ax.set_xlim(-750000,2000000)
ax.set_ylim([-2000000,500000])
plt.axis('off')

plt.savefig('min_land.tiff',dpi=300)
