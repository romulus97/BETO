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
df_geo_corn = pd.read_excel('combined_pivot_excel_electricity.xlsx',header=0, engine='openpyxl') #contains data sets for corn (state, land cost, yield etc)
df_geo_soy = pd.read_excel('combined_pivot_soy_excel_electricity.xlsx',header=0, engine='openpyxl') #contains data sets for soy (state, land cost, yield etc)
df_geo_grass = pd.read_excel('combined_pivot_grass_excel_electricity.xlsx',header=0, engine='openpyxl') #contains data sets for grass (state, land cost, yield etc) 
df_geo_algea = pd.read_excel('combined_pivot_algea_excel_electricity.xlsx',header=0, engine='openpyxl') #contains data sets for algae (state, land cost, yield etc) 

districts = list(df_geo_corn['STASD_N']) # list of ag_district code

df_ha =  pd.read_csv('Decision_Variables_borg_two_crop_trialdistrict.csv',header=0) #contains data sets for used hectare
df_O = pd.read_csv('Objective_Functions_borg_two_crop_trialdistrict.csv',header=0,index_col=0)

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
    
df_O.columns = ['cost','max_energy_shortfall','min_GHG_emission']


#sorting = df_O.sort_values(by='max_energy_shortfall', ascending=False)
#sorting = df_O.sort_values(by='min_GHG_emission', ascending=False)
sorting = df_O.sort_values(by='cost', ascending=False)


# MIN SOLUTION 
n = 1
min_n_cost = sorting.tail(n)
ind_min_cost = list(min_n_cost.index.values)

for ind in ind_min_cost:
    a = ind_min_cost.index(ind)

    CS = CS_total_MJ[ind]
    G = G_energy_total_MJ[ind]
    A = A_energy_total_MJ[ind]
    
    
    width = 0.8       # the width of the bars: can also be len(x) sequence
    fig, ax = plt.subplots(figsize=(8,5))
    
    
    abc = pd.DataFrame(zip(CS,G,A), index=labels)
    
    abc.plot(kind='bar', stacked=True, ax=ax, color = ['#023e8a','#ffbe0b','#d90429'])
    ax.legend('',frameon=False)
    ax.set_ylabel('Total Produced MJ', fontsize=15)
    ax.set_xlabel('Years', fontsize=15)
    
    ax.tick_params(axis='both', which='major', labelsize=12)
    ax.set_xticklabels(labels,rotation=40,fontsize=12)

    
    index = [str (b) for b in ind_min_cost]
    
    #ax.set_title('Minimum Quota Shortfall Solution',fontsize=15)
    #ax.set_title('Minimum GHG Intensity (tons $CO_{2}$) Solution',fontsize=15)
    ax.set_title('Minimum Cost Solution',fontsize=15)
    
    
    # ax.legend(bbox_to_anchor=(1.02, 1.05),loc=2, prop={'size': 7})
    
    leg1 = mpatches.Patch(color='#023e8a', label='Produced MJ \n from Corn/soy')
    leg2 = mpatches.Patch(color='#ffbe0b', label='Produced MJ \n from Grass')
    leg3 = mpatches.Patch(color='#d90429', label='Produced MJ \n from Algae')
    fig.legend(handles=[leg1,leg2,leg3],loc='center left', bbox_to_anchor=(1.04, 0.5), bbox_transform=ax.transAxes, borderpad=0.8)
    
    
    #fig.savefig(index[a] +' MJ_bar_chart_min_energy_shortfall.png',bbox_inches='tight', dpi=300)
    #fig.savefig(index[a] +' MJ_bar_chart_min_GHG_emission.png',bbox_inches='tight', dpi=300)
    fig.savefig(index[a] +' MJ_bar_chart_min_cost.png',bbox_inches='tight', dpi=300)
    
    plt.show()     

# MAX SOLUTION 
n = 1
max_n_cost = sorting.head(n)
ind_max_cost = list(max_n_cost.index.values)

for indm in ind_max_cost:
    am = ind_max_cost.index(indm)

    CSm = CS_total_MJ[indm]
    Gm = G_energy_total_MJ[indm]
    Am = A_energy_total_MJ[indm]
    
    
    width = 0.8       # the width of the bars: can also be len(x) sequence
    fig, ax = plt.subplots(figsize=(8,5))
    
    
    abcm = pd.DataFrame(zip(CSm,Gm,Am), index=labels)
    
    abcm.plot(kind='bar', stacked=True, ax=ax, color = ['#023e8a','#ffbe0b','#d90429'])
    ax.legend('',frameon=False,)
    ax.set_ylabel('Total Produced MJ', fontsize=15)
    ax.set_xlabel('Years', fontsize=15)
    
    ax.tick_params(axis='both', which='major', labelsize=12)
    ax.set_xticklabels(labels,rotation=40,fontsize=12)

    index = [str (b) for b in ind_max_cost]
    
    # ax.set_title(index[am] +' Maximum Quota Shortfall Solution')
    
    #ax.set_title('Maximum Quota Shortfall Solution',fontsize=15)
    #ax.set_title('Maximum GHG Intensity (tons $CO_{2}$) Solution',fontsize=15)
    ax.set_title('Maximum cost solution',fontsize=15)
    
    
    # ax.legend(bbox_to_anchor=(1.02, 1.05),loc=2, prop={'size': 7})
    
    leg1 = mpatches.Patch(color='#023e8a', label='Produced MJ \n from Corn/soy')
    leg2 = mpatches.Patch(color='#ffbe0b', label='Produced MJ \n from Grass')
    leg3 = mpatches.Patch(color='#d90429', label='Produced MJ \n from Algae')
    fig.legend(handles=[leg1,leg2,leg3],loc='center left', bbox_to_anchor=(1.04, 0.5), bbox_transform=ax.transAxes, borderpad=0.8)
    
    
    #fig.savefig(' MJ_bar_chart_max_energy_shortfall.png',bbox_inches='tight', dpi=300)
    #fig.savefig(index[am] +' MJ_bar_chart_max_GHG_emission.png',bbox_inches='tight', dpi=300)
    fig.savefig(index[am] +' MJ_bar_chart_max_cost.png',bbox_inches='tight', dpi=300)
    
    plt.show()    