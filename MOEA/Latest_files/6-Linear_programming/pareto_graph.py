# -*- coding: utf-8 -*-
"""
Created on Sat Apr 29 20:42:03 2023

@author: eari
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from mpl_toolkits.mplot3d import *
from random import random, seed
from matplotlib import cm


# Yields and land limits : contains State - STASD_N - land_limits_ha - yields (1998-2013)
df_geo_corn = pd.read_excel('combined_pivot_Corn.xlsx',header=0, engine='openpyxl')
df_geo_soy = pd.read_excel('combined_pivot_Soy.xlsx',header=0, engine='openpyxl')
df_geo_grass_AG = pd.read_excel('combined_pivot_AG_Switchgrass.xlsx',header=0, engine='openpyxl') 
df_geo_grass_ML = pd.read_excel('combined_pivot_ML_Switchgrass.xlsx',header=0, engine='openpyxl') 
df_geo_algae_AG = pd.read_excel('combined_pivot_AG_Algae.xlsx',header=0, engine='openpyxl')   
df_geo_algae_ML = pd.read_excel('combined_pivot_ML_Algae.xlsx',header=0, engine='openpyxl')  

# Greenhouse gas emission : contains State - STASD_N - greenhouse gas emission (gCO2/MJ) (1998-2013)
df_geo_corn_GHG= pd.read_excel('Corn_GHG.xlsx',header=0, engine='openpyxl') 
df_geo_soy_GHG = pd.read_excel('Soy_GHG.xlsx',header=0, engine='openpyxl') 
df_geo_grass_AG_GHG = pd.read_excel('Switchgrass_AG_GHG.xlsx',header=0, engine='openpyxl')
df_geo_grass_ML_GHG = pd.read_excel('Switchgrass_ML_GHG.xlsx',header=0, engine='openpyxl') 
df_geo_algae_AG_GHG = pd.read_excel('Algae_AG_GHG.xlsx',header=0, engine='openpyxl')
df_geo_algae_ML_GHG = pd.read_excel('Algae_ML_GHG.xlsx',header=0, engine='openpyxl')

# Minimum fuel selling price (MFSP) : contains State - STASD_N - MFSP ($/MJ) (1998-2013)
df_geo_corn_MFSP = pd.read_excel('Corn_MFSP.xlsx',header=0, engine='openpyxl')
df_geo_soy_MFSP = pd.read_excel('Soy_MFSP.xlsx',header=0, engine='openpyxl')
df_geo_grass_AG_MFSP = pd.read_excel('Switchgrass_AG_MFSP.xlsx',header=0, engine='openpyxl') 
df_geo_grass_ML_MFSP = pd.read_excel('Switchgrass_ML_MFSP.xlsx',header=0, engine='openpyxl')
df_geo_algae_AG_MFSP = pd.read_excel('Algae_AG_MFSP.xlsx',header=0, engine='openpyxl')
df_geo_algae_ML_MFSP = pd.read_excel('Algae_ML_MFSP.xlsx',header=0, engine='openpyxl')

# Corn Grain values 
C_yield = df_geo_corn.loc[:,1998:2013].values  #kg/ha
Corn_emission= df_geo_corn_GHG.loc[:,1998:2013].values  #gCO2/MJ
Corn_cost= df_geo_corn_MFSP.loc[:,1998:2013].values  #$/MJ

# Soybean values
S_yield = df_geo_soy.loc[:,1998:2013].values  #kg/ha
Soy_emission = df_geo_soy_GHG.loc[:,1998:2013].values  #gCO2/MJ
Soy_cost = df_geo_soy_MFSP.loc[:,1998:2013].values    #$/MJ

# Grass yield on marginal land 
G_yield_ML = df_geo_grass_ML.loc[:,1998:2013].values  #yield in kg/ha
Grass_emission_ML = df_geo_grass_ML_GHG.loc[:,1998:2013].values  #gCO2/MJ
Grass_cost_ML = df_geo_grass_ML_MFSP.loc[:,1998:2013].values    #$/MJ

# Algae yield on marginal lands 
A_yield_ML = df_geo_algae_ML.loc[:,1998:2013].values  #yield in kg/ha
Algae_emission_ML = df_geo_algae_ML_GHG.loc[:,1998:2013].values  #gCO2/MJ
Algae_cost_ML = df_geo_algae_ML_MFSP.loc[:,1998:2013].values    #$/MJ

# Grass values on agricultural lands 
G_yield_AG = df_geo_grass_AG.loc[:,1998:2013].values  #yield in kg/ha
Grass_emission_AG = df_geo_grass_AG_GHG.loc[:,1998:2013].values  #gCO2/MJ
Grass_cost_AG = df_geo_grass_AG_MFSP.loc[:,1998:2013].values    #$/MJ

# Algae yield on agricultural land
A_yield_AG = df_geo_algae_AG.loc[:,1998:2013].values  #yield in kg/ha
Algae_emission_AG = df_geo_algae_AG_GHG.loc[:,1998:2013].values  #gCO2/MJ
Algae_cost_AG = df_geo_algae_AG_MFSP.loc[:,1998:2013].values    #$/MJ

agricultural_land_limits = df_geo_corn['land_limits_ha'].values
num_c = np.size(agricultural_land_limits) #size of land limit 

# Year range from 1998 to 2013 
years = range(1998,2014)


biofuel_list = [20] #,6,9,12,15,18,20
bg = 20 ## We will try 0, 3, 6, 9, 12, 15, 18, 20   biofuel gallon 

bgg =  bg*10**9  # conversion to billion  
con = 30.81*(1/0.2641)  ## MJ/litre * liter/gallons   ## jet fuels conversion
quota = bgg*con  ## energy as MJ/yr
    


Z =[]


all_fuel_cost_weights = np.arange(0,1.05,0.05)
all_GHG_cost_weights = np.arange(0,1.05,0.05)
all_GHG_cost_weights[::-1].sort()
weight_length = len(all_GHG_cost_weights)

# biofuel_list = [3]
df_S = pd.DataFrame(list())

idx = 0


for bio_amount in biofuel_list:
    
    quota_change = bio_amount*0.02
    upper_bound = bio_amount + quota_change
    lower_bound = bio_amount - quota_change
    actual_quota_list = np.arange(lower_bound,upper_bound+0.01,0.01)
    
    for my_quota in actual_quota_list:
    
        my_quota = round(my_quota,3)
        
        for we_idx in range(0,weight_length):
            
            idx+=1
            
            cost_weight = all_fuel_cost_weights[we_idx]
            cost_weight = round(cost_weight,3)
            GHG_weight = all_GHG_cost_weights[we_idx]
            GHG_weight = round(GHG_weight,3)

            fn = f'Results/Land_usage/land_usage_out_district_level_{my_quota}_cost_{cost_weight}_GHG_{GHG_weight}_feasible.csv'     
            df_O = pd.read_csv(fn,header=0) #,index_col=0
            # df_O = df_O.T
            
            if idx==1:
                result = df_O
                
            else:
                
                result = pd.concat([result,df_O['Value']],axis=1)
                
        result.columns = ['Feedstock', 'District']+[*range(1,len(result.columns)-1)]      
        df_pareto =  result.iloc[:,2:]
        df_pareto = df_pareto.T
        
    solutions = range(0,len(df_pareto))
    Energy_total = np.zeros((len(years),1))
    Energy_solution = np.zeros((len(solutions)))
    Energy_shortfall = np.zeros((len(solutions)))
    GHG_impact_yearly = np.zeros((len(years),1))
    GHG_impact_solution = np.zeros((len(solutions)))
    MFSP_total_yearly = np.zeros((len(years),1))
    MFSP_total_solution = np.zeros((len(solutions)))


    for year in years:
        i = years.index(year)
        
        for s in solutions:
            ##############################
            # Cultivation and Harvesting
            #biomass production from used land for each district as kg  
            CG_prod = df_pareto.iloc[s,0:num_c]*C_yield[:,i]
            SB_prod = df_pareto.iloc[s,num_c:2*num_c]*S_yield[:,i]
            G_prod_ML = df_pareto.iloc[s,2*num_c:3*num_c]*G_yield_ML[:,i]
            A_prod_ML = df_pareto.iloc[s,3*num_c:4*num_c]*A_yield_ML[:,i]      
            G_prod_AG = df_pareto.iloc[s,4*num_c:5*num_c]*G_yield_AG[:,i]
            A_prod_AG = df_pareto.iloc[s,5*num_c:]*A_yield_AG[:,i]  
            
            
            # MJ conversion from kg biomass 
            Energy =sum(9.42 * CG_prod) + sum(8.02 * SB_prod) + sum(8.35* G_prod_ML) + sum(20.82* A_prod_ML) + sum(8.35* G_prod_AG) + sum(20.82*A_prod_AG)   
            Energy_total[i] = Energy   # total energy MJ/yr
            Energy_sol = sum(Energy_total)
            energy_short = sum(Energy_total)/len(years)
            Energy_solution[s] = Energy_sol
            Energy_shortfall[s] = energy_short
            
            # Greenhouse gas emission calculation 
            GHG_emission_corn = Corn_emission[:,i]*(9.42 * CG_prod)       
            GHG_emission_soy = Soy_emission[:,i]*(8.02 * SB_prod)     
            GHG_emission_grass_ML = Grass_emission_ML[:,i]*(8.35* G_prod_ML)
            GHG_emission_algae_ML = Algae_emission_ML[:,i]*(20.82* A_prod_ML)
            GHG_emission_grass_AG = Grass_emission_AG[:,i]*(8.35* G_prod_AG)
            GHG_emission_algae_AG = Algae_emission_AG[:,i]*(20.82* A_prod_AG)
            
            GHG_impact = sum(GHG_emission_corn)+ sum(GHG_emission_soy) + sum(GHG_emission_grass_ML) + sum(GHG_emission_algae_ML) + sum(GHG_emission_grass_AG) + sum(GHG_emission_algae_AG)
            GHG_impact_yearly[i] = GHG_impact
            GHG_impact_sol = sum(GHG_impact_yearly)
            GHG_impact_solution[s] = GHG_impact_sol
    
            
            MFSP_corn = Corn_cost[:,i]*(9.42 * CG_prod)
      
            MFSP_soy = Soy_cost[:,i]*(8.02 * SB_prod)
    
            MFSP_grass_ML = Grass_cost_ML[:,i]*(8.35* G_prod_ML)
    
            MFSP_algae_ML = Algae_cost_ML[:,i]*(20.82* A_prod_ML)
    
            MFSP_grass_AG = Grass_cost_AG[:,i]*(8.35* G_prod_AG)
    
            MFSP_algae_AG = Algae_cost_AG[:,i]*(20.82* A_prod_AG)
    
            MFSP_total = sum(MFSP_corn) + sum(MFSP_soy) + sum(MFSP_grass_ML) + sum(MFSP_algae_ML) + sum(MFSP_grass_AG) + sum(MFSP_algae_AG)
            MFSP_total_yearly[i] = MFSP_total
            MFSP_total_sol = sum(MFSP_total_yearly)
            MFSP_total_solution[s] = MFSP_total_sol
            
            min_MSFP = MFSP_total_solution/Energy_solution
            min_shortfall = Energy_shortfall-quota
            min_GHG = GHG_impact_solution/Energy_solution
            
            df_S['cost/MJ'] = min_MSFP
            df_S['energy_shortfall'] = min_shortfall
            df_S['GHG_emission/MJ'] = min_GHG
            
            
            # df_S['enegry'] = Energy_total
     
            colors = df_S['energy_shortfall']
            
            x = df_S['cost/MJ']
            y = df_S['energy_shortfall']
            z = df_S['GHG_emission/MJ']
            
            plt.rcParams['font.sans-serif'] = "Arial"
            plt.rcParams["font.weight"] = "bold"
            plt.rcParams["axes.labelweight"] = "bold"
            
            plt.rcParams.update({'font.size': 14})
            
            # fig, ax = plt.subplots(1,3, figsize=(13, 5.3),constrained_layout = True)
            plt.scatter(x, z, c=colors, cmap='plasma');
            # plt.savefig('Pareto_graph' + bio_amount + '.png',dpi=150, bbox_inches='tight')
            
            # # plt.show()
            
            # # colorbar_min = min(Energy_total)
            # # colorbar_max = max(Energy_total)
            
            # fig, ax = plt.subplots(1,3, figsize=(13, 5.3),constrained_layout = True)
            # fig.suptitle(b + v, fontsize=16)
            
            # colorbar_min = min(Energy_total)
            # colorbar_max = max(Energy_total)
            
            # ### Cost/MJ vs Energy shortfall
    
            # ax[0].scatter(x, y, c=colors, cmap='plasma');
            # ax[0].tick_params(axis='both', which='major', labelsize=14)
            # ax[0].set_xlabel('Cost ($/MJ)',fontsize=14)
            # ax[0].set_ylabel('Quota Shortfall (MJ)',fontsize=14)
    
            # axis_fontsize=14
            
            # ax[0].grid(False)
            
            
            # ### Cost/MJ vs GHG
            
            # ax[1].scatter(x, z, c=colors, cmap='plasma');
            # ax[1].tick_params(axis='both', which='major', labelsize=14)
            # ax[1].set_xlabel('Cost ($/MJ)',fontsize=14)
            # ax[1].set_ylabel(r'GHG Intensity (g $CO_{2}$ / MJ)',fontsize=14)
    
            # axis_fontsize=14
            
            # ax[1].grid(False)
            
            # ### GHG emission/MJ vs Energy shortfall
    
            # ax[2].scatter(z, y, c=colors, cmap='plasma');
            # ax[2].tick_params(axis='both', which='major', labelsize=14)
            # ax[2].set_xlabel(r'GHG Intensity (g $CO_{2}$ / MJ)',fontsize=14)
            # ax[2].set_ylabel('Quota Shortfall (MJ)',fontsize=14)
    
            # axis_fontsize=14
            
            # ax[2].grid(False)
            # ax[2].legend()
    
            
            # cb_ax = fig.add_axes([1.05,.1,.015,0.8])
            # fig.colorbar(mpl.cm.ScalarMappable(norm=mpl.colors.Normalize(vmin=colorbar_min, vmax=colorbar_max), cmap='plasma'),orientation='vertical',cax=cb_ax)
            # cb_ax.set_ylabel('Energy Production (MJ)',fontsize=14, rotation=270, labelpad = 15)
            
            # plt.savefig('Pareto_graph_district' + b + v + '.png',dpi=150, bbox_inches='tight')
    
        
        

        
    

