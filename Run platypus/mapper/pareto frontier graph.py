# -*- coding: utf-8 -*-
"""
Created on Wed Feb  2 00:07:04 2022

@author: Ece Ari Akdemir
"""

import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.io as pio
pio.renderers.default='browser'
import plotly.express as px
import pandas as pd
import numpy as np
import plotly.express as px

version = 'district'


# import excel sheet  
df_geo_corn = pd.read_excel('combined_pivot_excel_electricity.xlsx',header=0, engine='openpyxl') #contains data sets for corn (state, land cost, yield etc)
df_geo_soy = pd.read_excel('combined_pivot_soy_excel_electricity.xlsx',header=0, engine='openpyxl') #contains data sets for soy (state, land cost, yield etc)
df_geo_grass = pd.read_excel('combined_pivot_grass_excel_electricity.xlsx',header=0, engine='openpyxl') #contains data sets for grass (state, land cost, yield etc) 
df_geo_algea = pd.read_excel('combined_pivot_algea_excel_electricity.xlsx',header=0, engine='openpyxl') #contains data sets for algae (state, land cost, yield etc) 

districts = list(df_geo_corn['STASD_N']) # list of ag_district code

df_ha =  pd.read_csv('Decision_Variables_borg_two_crop_trialdistrict.csv',header=0) #contains data sets for used hectare

C_ha = np.transpose(df_ha).iloc[1:108].values # used hectare for corn 
S_ha = np.transpose(df_ha).iloc[1:108].values # used hectare for soy
G_ha = np.transpose(df_ha).iloc[108:215].values # used hectare for grass
A_ha = np.transpose(df_ha).iloc[215:].values # used hectare for algae

LC = df_geo_corn.loc[:,'land_costs-$/ha'].values # $ per ha

years = range(1998,2014)
solution = range(len(df_ha))


# Corn Grain yield
C_yield = df_geo_corn.loc[:,1998:2013].values  #yield in kg/ha

# Soybean yield
S_yield = df_geo_soy.loc[:,1998:2013].values  #yield in kg/ha

# Grass yield
G_yield = df_geo_grass.loc[:,1998:2013].values  #yield in kg/ha

# Algea yield
A_yield = df_geo_algea.loc[:,1998:2013].values  #yield in kg/ha

num_c = np.size(LC) #size of land cost 
Energy_total = np.zeros((len(years),1))


CG_kg_tot = np.zeros((1,len(df_ha)))
SB_kg_tot = np.zeros((1,len(df_ha)))
G_kg_tot = np.zeros((1,len(df_ha)))
A_kg_tot = np.zeros((1,len(df_ha)))

Y = C_yield[:,15]   # corn yield kg/ha
S = S_yield[:,15]   # soy yield kg/ha
G = G_yield[:,15]   # grass yield kg/ha
A = A_yield[:,15]   # algae yield kg/ha

for s in solution:
    CG_prod = sum(C_ha[:,s]*Y) 
    CG_kg_tot[:,s] = CG_prod         # total corn biomass production (kg)
        
    SB_prod = sum(S_ha[:,s]*S)
    SB_kg_tot[:,s] = SB_prod         # total soy biomass production (kg)
        
        
    G_prod = sum(G_ha[:,s]*G)
    G_kg_tot[:,s] = G_prod           # total grass biomass production (kg)
        
    A_prod = sum(A_ha[:,s]*A)
    A_kg_tot[:,s] = A_prod           # total algae biomass production (kg)

CG_total = np.transpose(CG_kg_tot)
SB_total = np.transpose(SB_kg_tot)
G_total = np.transpose(G_kg_tot)
A_total = np.transpose(A_kg_tot)

Total = CG_total + SB_total + G_total + A_total


#objective function
fn = 'Objective_Functions_borg_two_crop_trial' + version + '.csv'
df_O = pd.read_csv(fn,header=0,index_col=0)
df_O.columns = ['cost','max_energy_shortfall','min_GHG_emission']
df_O['kg'] = Total

r = []
t = []
l = []
nd = []

# R = 100000000000000000
# T = 100000000000000000
# L = 100000000000000000

for i in range(0,len(df_O)):
    if i < 1:
        r.append(df_O.loc[i,'max_energy_shortfall']/(10**9))
        t.append(df_O.loc[i,'min_GHG_emission']/(10**11))
        l.append(df_O.loc[i,'cost']/(10**13))
        nd.append(i)
    else:
        n = 1
        for j in r:
            idx = r.index(j)
            if r[idx] < df_O.loc[i,'max_energy_shortfall']/(10**9) and t[idx] < df_O.loc[i,'min_GHG_emission']/(10**11) and l[idx] < df_O.loc[i,'cost']/(10**13):
                n = 0
        if n > 0:
            r.append(df_O.loc[i,'max_energy_shortfall']/(10**9))
            t.append(df_O.loc[i,'min_GHG_emission']/(10**11))   
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


# fig = plt.figure()
# ax = fig.add_subplot(projection='3d')

# p = ax.scatter(r,t,l, c=r, s=l, cmap='hot',linewidth=1, edgecolor='black')
# # fig.colorbar(p, ax=ax)
# fig.colorbar(p, ax=ax, location='left', shrink=0.6)
# ax.scatter(r,t,l,)

# plt.figure()
# plt.scatter(r,t)
# ax.set_xlabel('max_energy_shortfall',fontweight='bold', fontsize=10)
# ax.set_ylabel('energy_changes',fontweight='bold',fontsize=10)
# ax.set_zlabel('cost',fontweight='bold',fontsize=10)

# plt.savefig('pareto.tiff',dpi = 330)

fig = px.scatter_3d(df_O, x='cost', y='max_energy_shortfall', z='min_GHG_emission',color='min_GHG_emission', size='kg', hover_data=['kg'])
fig.update_layout(title='Comparison max_energy_shortfall,min_GHG_emission and cost')
# fig3.update_layout( height = 900, width = 1000,title='Comparison Biofuel cost-shortfall-Land usage(ha) and ethanol changes')
fig.show()
fig.write_html("Comparison max_energy_shortfall,min_GHG_emission and cost.html")









