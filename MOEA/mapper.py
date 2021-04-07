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

import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import geopandas as gpd
from shapely.geometry import Point, Polygon


df = pd.read_csv('GPS_20_Hubs.csv',header=0)
crs = {'init':'epsg:4326'}
# crs = {"init": "epsg:2163"}
geometry = [Point(xy) for xy in zip(df['Longitude'],df['Latitude'])]
geo_df = gpd.GeoDataFrame(df,crs=crs,geometry=geometry)
geo_df = geo_df.to_crs(epsg=2163)

state_map = gpd.read_file('shapefiles/geo_export_9ef76f60-e019-451c-be6b-5a879a5e7c07.shp')
state_map = state_map.to_crs(epsg=2163)

group_map = gpd.read_file('shapefiles/Corn_belt_all_states_20_bz.shp')
group_map = group_map.to_crs(epsg=2163)

county_map = gpd.read_file('shapefiles/Corn_belt_all_states.shp')
county_map = county_map.to_crs(epsg=2163)

county_map2 = gpd.read_file('shapefiles/USA_counties.shp')
county_map2 = county_map2.to_crs(epsg=2163)

cb_counties = gpd.clip(county_map2,county_map)

fig,ax = plt.subplots()
state_map.plot(ax=ax,color='gray',alpha=0.6,edgecolor='white',linewidth=0.5)
cb_counties.plot(ax=ax,color='orange',alpha=1,edgecolor='darkslategrey',linewidth=0.2)   

ax.set_box_aspect(1)
ax.set_xlim(-750000,2000000)
ax.set_ylim([-2000000,500000])
plt.axis('off')

plt.savefig('county.tiff',dpi=300)

fig,ax = plt.subplots()
state_map.plot(ax=ax,color='gray',alpha=0.6,edgecolor='white',linewidth=0.5)
group_map.plot(ax=ax,color='paleturquoise',alpha=1,edgecolor='black',linewidth=0.2)

ax.set_box_aspect(1)
ax.set_xlim(-750000,2000000)
ax.set_ylim([-2000000,500000])
plt.axis('off')

plt.savefig('groups.tiff',dpi=300)

fig,ax = plt.subplots()
state_map.plot(ax=ax,color='gray',alpha=0.6,edgecolor='white',linewidth=0.5)
cb_counties.plot(ax=ax,color='orange',alpha=1,edgecolor='darkslategrey',linewidth=0.2)   
group_map.plot(ax=ax,color='none',alpha=1,edgecolor='black',linewidth=0.5)

for i in range(1,20):
    geo_df[geo_df['hub']==i].plot(ax=ax,markersize=16,color='black',marker='o',edgecolor='white',linewidth=0.1)

ax.set_box_aspect(1)
ax.set_xlim(-750000,2000000)
ax.set_ylim([-2000000,500000])
plt.axis('off')

plt.savefig('hubs.tiff',dpi=300)


# map subset of counties

# import county level data
df_subset = pd.read_csv('geodata_total.csv',header=0)
sub_fips = list(df_subset['fips'])
cb_counties = cb_counties.reset_index(drop=True)
# drop any redundant lines
FIPS = []
for i in range(0,len(cb_counties)):
    f = float(cb_counties.loc[i,'FIPS'])
    if f in sub_fips:
        pass
    else:
        cb_counties = cb_counties.drop(i)

cb_counties = cb_counties.reset_index(drop=True)
    

fig,ax = plt.subplots()
state_map.plot(ax=ax,color='gray',alpha=0.6,edgecolor='white',linewidth=0.5)
cb_counties.plot(ax=ax,color='orange',alpha=1,edgecolor='darkslategrey',linewidth=0.2)   
group_map.plot(ax=ax,color='none',alpha=1,edgecolor='black',linewidth=0.5)

# for i in range(0,len(df_subset)):
       
#     c = df_subset.loc[i,'fips']
    
#     sample = county_map2.loc[county_map2['FIPS'] == c]
#     sample.plot(ax=ax,color='white',alpha=1,edgecolor='magenta',linewidth=0.8)
                      

for i in range(1,20):
    geo_df[geo_df['hub']==i].plot(ax=ax,markersize=16,color='black',marker='o',edgecolor='white',linewidth=0.1)

# for i in [4,8,10]:
#     geo_df[geo_df['hub']==i].plot(ax=ax,markersize=32,color='deepskyblue',marker='o',edgecolor='blue',linewidth=0.1)
        
ax.set_box_aspect(1)
ax.set_xlim(-750000,2000000)
ax.set_ylim([-2000000,500000])
plt.axis('off')

plt.savefig('subset.tiff',dpi=300)


#objective function
df_O = pd.read_csv('Objective_Functions_all_2000_1.csv',header=0,index_col=0)
df_O.columns = ['ref_capex','trans_opex']

r = []
t = []
nd = []

R = 10000000000000
T = 10000000000000

for i in range(0,len(df_O)):
    if i < 1:
        r.append(df_O.loc[i,'ref_capex']/1000000000)
        t.append(df_O.loc[i,'trans_opex']/1000000000)
        nd.append(i)
    else:
        n = 1
        for j in r:
            idx = r.index(j)
            if r[idx] < df_O.loc[i,'ref_capex']/1000000000 and t[idx] < df_O.loc[i,'trans_opex']/1000000000:
                n = 0
        if n > 0:
            r.append(df_O.loc[i,'ref_capex']/1000000000)
            t.append(df_O.loc[i,'trans_opex']/1000000000)    
            nd.append(idx)
    for i in r:
        idx = r.index(i)
        if r[0] > r[idx] and t[0] > t[idx]:
            r.pop(0)
            t.pop(0)
            
plt.figure()
plt.scatter(r,t)
plt.xlabel('Biofinery Capex $B',fontweight='bold',fontsize=12)
plt.ylabel('Transporation Opex $B',fontweight='bold',fontsize=12)

plt.savefig('pareto.tiff',dpi = 330)
    
    
#decision variables
df_D = pd.read_csv('Decision_Variables_all_2000_1.csv',header=0,index_col=0)


#minimum capex
d_sample = list(df_D.iloc[1,0:len(df_subset)])
cmap = matplotlib.cm.get_cmap('cool')
M = max(d_sample)


fig,ax = plt.subplots()
state_map.plot(ax=ax,color='gray',alpha=0.6,edgecolor='white',linewidth=0.5)
cb_counties.plot(ax=ax,color='white',alpha=1,edgecolor='darkslategrey',linewidth=0.2)   
# group_map.plot(ax=ax,color='none',alpha=1,edgecolor='black',linewidth=0.5)

# plt.savefig('min_ref_capex.tiff',dpi=300)
C = []
for i in range(0,len(cb_counties)):
    f = float(cb_counties.loc[i,'FIPS'])
    idx = sub_fips.index(f)
    if not idx:
        C.append(0)
    else:
        d_value = d_sample[idx]
        sample_c = cmap(d_value/M)
        hexa = matplotlib.colors.rgb2hex(sample_c)
        C.append(hexa)
        
cb_counties['color'] = C
cb_counties.plot(ax=ax,color=list(cb_counties['color']),alpha=1,edgecolor='none',linewidth=0.8)

# STOPPED HERE

#plot refineries
# d_sample = list(df_D.iloc[1,len(df_subset):])
# dvs = int(np.sqrt(len(d_sample)))
# mx = max(d_sample)
# for i in range(0,len(d_sample)):
#     d_sample[i] = (d_sample[i]/mx)*3
    
# geo_df['marker_size'] = d_sample

# for i in range(1,len(geo_df)):
#     geo_df[geo_df['hub']==i].plot(ax=ax,markersize=geo_df['marker_size'],color="None",marker='o',edgecolor='black',linewidth=1)


ax.set_box_aspect(1)
ax.set_xlim(-750000,2000000)
ax.set_ylim([-2000000,500000])
plt.axis('off')

plt.savefig('min_ref_capex.tiff',dpi=300)