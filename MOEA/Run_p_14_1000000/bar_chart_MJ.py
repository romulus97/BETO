# -*- coding: utf-8 -*-
"""
Created on Sat Jun  4 15:26:38 2022

@author: eari
"""

import matplotlib.pyplot as plt

import pandas as pd
import numpy as np
import plotly.io as pio
pio.renderers.default='browser'
import plotly.express as px
import corn_grain_processing as CG_processing
import soybean_processing as SB_processing 
import Pyrol_processing as G_processing 
import Algal_Oil as A_processing
import matplotlib.patches as mpatches


labels = ['1998', '1999', '2000', '2001', '2002', '2003', '2004', '2005', '2006', '2007', '2008', '2009', '2010', '2011', '2012', '2013']

version = 'district'


# import excel sheet  
df_geo_corn = pd.read_excel('combined_pivot_corn_excel_electricity.xlsx',header=0, engine='openpyxl') #contains data sets for corn (state, land cost, yield etc)
df_geo_soy = pd.read_excel('combined_pivot_soy_excel_electricity.xlsx',header=0, engine='openpyxl') #contains data sets for soy (state, land cost, yield etc)
df_geo_grass = pd.read_excel('combined_pivot_grass_excel_electricity.xlsx',header=0, engine='openpyxl') #contains data sets for grass (state, land cost, yield etc) 
df_geo_algae = pd.read_excel('combined_pivot_algae_excel_electricity.xlsx',header=0, engine='openpyxl') #contains data sets for algae (state, land cost, yield etc) 

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

# Algae yield
A_yield = df_geo_algae.loc[:,1998:2013].values  #yield in kg/ha

num_c = np.size(LC) #size of land cost 
Energy_total = np.zeros((len(years),1))


CG_kg_tot = np.zeros((1,len(df_ha)))
SB_kg_tot = np.zeros((1,len(df_ha)))
G_kg_tot = np.zeros((1,len(df_ha)))
A_kg_tot = np.zeros((1,len(df_ha)))

CG_kg_tot_den = np.zeros((len(years),len(df_ha)))
SB_kg_tot_den = np.zeros((len(years),len(df_ha)))
G_kg_tot_den = np.zeros((len(years),len(df_ha)))
A_kg_tot_den = np.zeros((len(years),len(df_ha)))

CG_kg_tot_dd = np.zeros((1,len(df_ha)))
SB_kg_tot_dd = np.zeros((1,len(df_ha)))
G_kg_tot_dd = np.zeros((1,len(df_ha)))
A_kg_tot_dd = np.zeros((1,len(df_ha)))



CG_ethanol_total_MJ = np.zeros((len(df_ha),len(years)))
SB_oil_total_MJ = np.zeros((len(df_ha),len(years)))
CS_total_MJ = np.zeros((len(df_ha),len(years)))
G_energy_total_MJ = np.zeros((len(df_ha),len(years)))
A_energy_total_MJ = np.zeros((len(df_ha),len(years)))

# Energy_total = np.zeros((len(solution),1))

for year in years:
    i = years.index(year)
    Y = C_yield[:,i]   # corn yield kg/ha
    S = S_yield[:,i]   # soy yield kg/ha
    G = G_yield[:,i]   # grass yield kg/ha
    A = A_yield[:,i]   # algae yield kg/ha
       

    for s in solution:
        CG_prod = sum(C_ha[:,s]*Y) 
        CG_kg_tot[:,s] = CG_prod         # total corn biomass production (kg)
        
        SB_prod = sum(S_ha[:,s]*S)
        SB_kg_tot[:,s] = SB_prod         # total soy biomass production (kg)
        
        
        G_prod = sum(G_ha[:,s]*G)
        G_kg_tot[:,s] = G_prod           # total grass biomass production (kg)
            
        A_prod = sum(A_ha[:,s]*A)
        A_kg_tot[:,s] = A_prod           # total algae biomass production (kg)
        
    CG_kg_tot_den[i] = CG_kg_tot
    SB_kg_tot_den[i] = SB_kg_tot
    G_kg_tot_den[i] = G_kg_tot
    A_kg_tot_den[i] = A_kg_tot
    
    for s in solution:
    
        CG_ethanol = CG_processing.sim(CG_kg_tot_den[:,s]) #kg ethanol
        CG_ethanol_total_MJ[s] = CG_ethanol*29.7   #MJ/kg
        
    
        SB_oil = SB_processing.sim(SB_kg_tot_den[:,s])  #kg soy oil
        SB_oil_total_MJ[s] = SB_oil*39.6           #MJ/kg
        
        CS_total_MJ[s] = CG_ethanol*29.7 + SB_oil*39.6   #MJ
        
        G_energy = G_processing.sim(G_kg_tot_den[:,s]) # kg biocrude 
        G_energy_total_MJ[s] = G_energy*21         #MJ
        
        A_energy = A_processing.sim(A_kg_tot_den[:,s]) # kg algae oil
        A_energy_total_MJ[s] = A_energy*22         #MJ
    
## max energy shortfall 
#i = 54
## min_GHG_emission
#i = 4787
## min_cost
i = 7368

CS = CS_total_MJ[i]
G = G_energy_total_MJ[i]
A = A_energy_total_MJ[i]


width = 0.8       # the width of the bars: can also be len(x) sequence
fig, ax = plt.subplots(figsize=(8,5))


abc = pd.DataFrame(zip(CS,G,A), index=labels)

abc.plot(kind='bar', stacked=True, ax=ax, color = ['#2b9348','#ffba08','#d00000'])
ax.legend('',frameon=False)
ax.set_ylabel('MJ', fontsize=10)
ax.set_xlabel('years', fontsize=10)

ax.tick_params(axis='both', which='major', labelsize=7)
ax.set_xticklabels(labels,rotation=360)

#ax.set_title('Min energy shortfall solution')
#ax.set_title('Min GHG emission solution')
ax.set_title('Min cost solution as percentage')


# ax.legend(bbox_to_anchor=(1.02, 1.05),loc=2, prop={'size': 7})

leg1 = mpatches.Patch(color='#2b9348', label='Corn/soy \nof MJ')
leg2 = mpatches.Patch(color='#ffba08', label='Grass \nof MJ')
leg3 = mpatches.Patch(color='#d00000', label='Algae \nof MJ')
fig.legend(handles=[leg1,leg2,leg3],loc='center left', bbox_to_anchor=(1.04, 0.5), bbox_transform=ax.transAxes, borderpad=0.8)


#fig.savefig('MJ_bar_chart_min_energy_shortfall.png',bbox_inches='tight', dpi=300)
#fig.savefig('MJ_bar_chart_min_GHG_emission.png',bbox_inches='tight', dpi=300)
#fig.savefig('MJ_bar_chart_min_cost.png',bbox_inches='tight', dpi=300)

plt.show()     

    