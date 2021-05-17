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

version = 'all'

import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import geopandas as gpd
from shapely.geometry import Point, Polygon

groups = 20
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

for i in range(1,groups):
    geo_df[geo_df['hub']==i].plot(ax=ax,markersize=16,color='black',marker='o',edgecolor='white',linewidth=0.1)

ax.set_box_aspect(1)
ax.set_xlim(-750000,2000000)
ax.set_ylim([-2000000,500000])
plt.axis('off')

plt.savefig('hubs.tiff',dpi=300)


# map subset of counties

# import county level data
df_subset = pd.read_csv('geodata_total.csv',header=0)
counties = list(df_subset['co_state'])

#county-to-hub data
filename = 'C2H_' + str(groups) + '.csv'
df_C2H = pd.read_csv(filename,header=0)
c = list(df_C2H['co_state'])

#eliminate and counties that don't appear in both lists
for i in counties:
    idx = counties.index(i)
    if i in c:
        pass
    else:
        df_subset= df_subset.drop(index=idx)

df_subset = df_subset.reset_index(drop=True)


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


for i in range(1,groups):
    geo_df[geo_df['hub']==i].plot(ax=ax,markersize=16,color='black',marker='o',edgecolor='white',linewidth=0.1)

      
ax.set_box_aspect(1)
ax.set_xlim(-750000,2000000)
ax.set_ylim([-2000000,500000])
plt.axis('off')

plt.savefig('subset.tiff',dpi=300)


#objective function
fn = 'Objective_Functions_' + version + '.csv'
df_O = pd.read_csv(fn,header=0,index_col=0)
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
fn = 'Decision_Variables_' + version + '.csv'
df_D = pd.read_csv(fn,header=0,index_col=0)


#minimum capex
d_sample = list(df_D.iloc[1,0:len(df_subset)])
cmap = matplotlib.cm.get_cmap('cool')
# M = max(d_sample)
M = np.max(df_D.iloc[:,0:len(df_subset)].values)

# plt.savefig('min_ref_capex.tiff',dpi=300)
C = []
fractions = []
sample_Cs = []
for i in range(0,len(cb_counties)):
    f = float(cb_counties.loc[i,'FIPS'])
    idx = sub_fips.index(f)
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
            C.append(C[-1])
    else:
        d_value = d_sample[idx]
        fraction = d_value/M
        fractions.append(fraction)
        sample_c = cmap(fraction)
        sample_Cs.append(sample_c)
        hexa = matplotlib.colors.rgb2hex(sample_c)
        C.append(hexa)
        
cb_counties['color'] = C

d_sample = list(df_D.iloc[1,len(df_subset):])
dvs = int(np.sqrt(len(d_sample)))
refinery_flow = np.zeros((dvs,))
for i in range(0,dvs):
    for j in range(0,dvs):
        f = d_sample[i*19+j]
        refinery_flow[j] += f

mx = np.max(df_D.iloc[:,len(df_subset):].values)

for i in range(0,dvs):
    refinery_flow[i] = (refinery_flow[i]/mx)*16

geo_df['marker_size'] = refinery_flow

fig,ax = plt.subplots()

state_map.plot(ax=ax,color='gray',alpha=0.6,edgecolor='white',linewidth=0.5)
cb_counties.plot(ax=ax,color='white',alpha=1,edgecolor='darkslategrey',linewidth=0.2)   
cb_counties.plot(ax=ax,color=list(cb_counties['color']),alpha=1,edgecolor='none',linewidth=0.8)

# plot refineries
geo_df.plot(ax=ax,markersize=geo_df['marker_size'],color="None",marker='o',edgecolor='black',linewidth=1)


ax.set_box_aspect(1)
ax.set_xlim(-750000,2000000)
ax.set_ylim([-2000000,500000])
plt.axis('off')

plt.savefig('example.tiff',dpi=300)


#minimum travel opex
d_sample = list(df_D.iloc[0,0:len(df_subset)])
cmap = matplotlib.cm.get_cmap('cool')
# M = max(d_sample)

# plt.savefig('min_ref_capex.tiff',dpi=300)
C = []
fractions = []
sample_Cs = []
for i in range(0,len(cb_counties)):
    f = float(cb_counties.loc[i,'FIPS'])
    idx = sub_fips.index(f)
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
            C.append(C[-1])
    else:
        d_value = d_sample[idx]
        fraction = d_value/M
        fractions.append(fraction)
        sample_c = cmap(fraction)
        sample_Cs.append(sample_c)
        hexa = matplotlib.colors.rgb2hex(sample_c)
        C.append(hexa)
        
cb_counties['color'] = C

d_sample = list(df_D.iloc[0,len(df_subset):])
dvs = int(np.sqrt(len(d_sample)))
refinery_flow = np.zeros((dvs,))
for i in range(0,dvs):
    for j in range(0,dvs):
        f = d_sample[i*19+j]
        refinery_flow[j] += f

# mx = max(refinery_flow)
for i in range(0,dvs):
    refinery_flow[i] = (refinery_flow[i]/mx)*16

geo_df['marker_size'] = refinery_flow

fig,ax = plt.subplots()

state_map.plot(ax=ax,color='gray',alpha=0.6,edgecolor='white',linewidth=0.5)
cb_counties.plot(ax=ax,color='white',alpha=1,edgecolor='darkslategrey',linewidth=0.2)   
cb_counties.plot(ax=ax,color=list(cb_counties['color']),alpha=1,edgecolor='none',linewidth=0.8)

# plot refineries
geo_df.plot(ax=ax,markersize=geo_df['marker_size'],color="None",marker='o',edgecolor='black',linewidth=1)


ax.set_box_aspect(1)
ax.set_xlim(-750000,2000000)
ax.set_ylim([-2000000,500000])
plt.axis('off')

plt.savefig('example2.tiff',dpi=300)