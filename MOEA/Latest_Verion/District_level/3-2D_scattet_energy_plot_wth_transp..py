# -*- coding: utf-8 -*-
"""
Created on Thu Jun 30 12:41:01 2022

@author: eari
"""


import matplotlib.pyplot as plt
plt.style.use('seaborn-whitegrid')
import numpy as np
import pandas as pd
from pysal.lib import weights
import geopandas as gpd
from pysal.explore import esda
import matplotlib as mpl

# billion = ['3','6','9','12']
# version = ['_100000_0.1district']  

billion = ['3','6','9','12','15','18','20']
version = ['_100000_0.001district', '_1000000_0.1district','_1000000_0.001district','_10000000_0.001district'] #,'_10000000_0.1district'


for b in billion:
    
    for v in version:
        
        fn = 'Objective_functions_borg_crops_GHG' + b + v + '_PARETO' +'.csv'
           
        df_O = pd.read_csv(fn,header=0,index_col=0)
        df_O.columns = ['cost','energy_shortfall','GHG_emission']
        

        district_map = gpd.read_file('shapefiles/AgD Corn belt.shp')
        district_map = district_map.to_crs(epsg=2163)

        ## CALCULATING ENERGY
        # import excel sheet  
        df_geo_corn = pd.read_excel('Platypus_codes/combined_pivot_Corn.xlsx',header=0, engine='openpyxl') #contains data sets for corn (state, land cost, yield etc)
        df_geo_soy = pd.read_excel('Platypus_codes/combined_pivot_Soy.xlsx',header=0, engine='openpyxl') #contains data sets for soy (state, land cost, yield etc)
        df_geo_grass_L = pd.read_excel('Platypus_codes/combined_pivot_AG_Switchgrass.xlsx',header=0, engine='openpyxl') #contains data sets for grass (state, land cost, yield etc) 
        df_geo_grass = pd.read_excel('Platypus_codes/combined_pivot_ML_Switchgrass.xlsx',header=0, engine='openpyxl') #contains data sets for grass (state, land cost, yield etc) 
        df_geo_algae_L = pd.read_excel('Platypus_codes/combined_pivot_AG_Algae.xlsx',header=0, engine='openpyxl') #contains data sets for algae (state, land cost, yield etc)   
        df_geo_algea = pd.read_excel('Platypus_codes/combined_pivot_ML_Algae.xlsx',header=0, engine='openpyxl') #contains data sets for algae (state, land cost, yield etc) 


        fn_ha = 'Decision_Variables_borg_crops_GHG' + b + v + '_PARETO' +'.csv'
        
        df_ha = pd.read_csv(fn_ha,header=0,index_col=0)
        
        num_c = len(df_geo_corn)
        
        ## Dividing corn, soy, grass and algae yield data.
        C_ha = np.transpose(df_ha).iloc[0:num_c].values # used hectare for corn 
        S_ha = np.transpose(df_ha).iloc[0:num_c].values # used hectare for soy
        G_ha = np.transpose(df_ha).iloc[num_c:2*num_c].values # used hectare for grass
        A_ha = np.transpose(df_ha).iloc[2*num_c:3*num_c].values # used hectare for algae
        G_ha_L = np.transpose(df_ha).iloc[3*num_c:4*num_c].values # used hectare for grass
        A_ha_L = np.transpose(df_ha).iloc[4*num_c:].values # used hectare for algae
        
        G_ha = np.zeros((1,len(df_ha)))
        A_ha = np.zeros((1,len(df_ha)))
        G_ha_L = np.zeros((1,len(df_ha)))
        A_ha_L = np.zeros((1,len(df_ha)))
        
        LL = df_geo_corn['land_limits_ha'].values
        
        years = range(1998,2014)
        solution = range(len(df_ha))
        
        # Corn Grain yield
        C_yield = df_geo_corn.loc[:,1998:2013].values  #yield in kg/ha
        
        # Soybean yield
        S_yield = df_geo_soy.loc[:,1998:2013].values  #yield in kg/ha
        
        # Grass yield
        G_yield_L = df_geo_grass_L.loc[:,1998:2013].values  #yield in kg/ha
        
        G_yield = df_geo_grass.loc[:,1998:2013].values  #yield in kg/ha
        
        # Algea yield
        A_yield_L = df_geo_algae_L.loc[:,1998:2013].values  #yield in kg/ha
        
        A_yield = df_geo_algea.loc[:,1998:2013].values  #yield in kg/ha
        
        num_c = np.size(LL) #size of land cost 
        Energy_total = np.zeros((len(years),1))
        
        
        CG_kg_tot = np.zeros((1,len(df_ha)))
        SB_kg_tot = np.zeros((1,len(df_ha)))
        G_kg_tot = np.zeros((1,len(df_ha)))
        A_kg_tot = np.zeros((1,len(df_ha)))
        G_kg_tot_L = np.zeros((1,len(df_ha)))
        A_kg_tot_L = np.zeros((1,len(df_ha)))
        
        CG_kg_tot_den = np.zeros((len(years),len(df_ha)))
        SB_kg_tot_den = np.zeros((len(years),len(df_ha)))
        G_kg_tot_den = np.zeros((len(years),len(df_ha)))
        A_kg_tot_den = np.zeros((len(years),len(df_ha)))
        G_kg_tot_den_L = np.zeros((len(years),len(df_ha)))
        A_kg_tot_den_L = np.zeros((len(years),len(df_ha)))
        
        
        CG_kg_tot_dd = np.zeros((1,len(df_ha)))
        SB_kg_tot_dd = np.zeros((1,len(df_ha)))
        G_kg_tot_dd = np.zeros((1,len(df_ha)))
        A_kg_tot_dd = np.zeros((1,len(df_ha)))
        G_kg_tot_dd_L = np.zeros((1,len(df_ha)))
        A_kg_tot_dd_L = np.zeros((1,len(df_ha)))
        
        
        for year in years:
            i = years.index(year)
            Y = C_yield[:,i]   # corn yield kg/ha
            S = S_yield[:,i]   # soy yield kg/ha
            G = G_yield[:,i]   # grass yield kg/ha
            A = A_yield[:,i]   # algae yield kg/ha
            G_L = G_yield_L[:,i]   # grass yield kg/ha
            A_L = A_yield_L[:,i]   # algae yield kg/ha
               
        
            for s in solution:
                CG_prod = sum(C_ha[:,s]*Y) 
                CG_kg_tot[:,s] = CG_prod         # total corn biomass production (kg)
                
                SB_prod = sum(S_ha[:,s]*S)
                SB_kg_tot[:,s] = SB_prod         # total soy biomass production (kg)
                
                
                G_prod = sum(G_ha[:,s]*G)
                G_kg_tot[:,s] = G_prod           # total grass biomass production (kg)
                    
                A_prod = sum(A_ha[:,s]*A)
                A_kg_tot[:,s] = A_prod           # total algae biomass production (kg)
                
                G_prod_L = sum(G_ha_L[:,s]*G_L)
                G_kg_tot_L[:,s] = G_prod_L           # total grass biomass production (kg)
                    
                A_prod_L = sum(A_ha_L[:,s]*A_L)
                A_kg_tot_L[:,s] = A_prod_L           # total algae biomass production (kg)
                
            CG_kg_tot_den[i] = CG_kg_tot
            SB_kg_tot_den[i] = SB_kg_tot
            G_kg_tot_den[i] = G_kg_tot
            A_kg_tot_den[i] = A_kg_tot
            G_kg_tot_den_L[i] = G_kg_tot_L
            A_kg_tot_den_L[i] = A_kg_tot_L
            
            for s in solution:
                CG_dd = sum(CG_kg_tot_den[:,s])
                CG_kg_tot_dd[:,s] = CG_dd/len(years)       # average corn biomass production for 15 years (kg)
                
                SB_dd = sum(SB_kg_tot_den[:,s])
                SB_kg_tot_dd[:,s] = SB_dd/len(years)       # average soy biomass production for 15 years (kg)
                
                G_dd = sum(G_kg_tot_den[:,s])
                G_kg_tot_dd[:,s] = G_dd/len(years)        # average grass biomass production for 15 years (kg)
                
                A_dd = sum(A_kg_tot_den[:,s])
                A_kg_tot_dd[:,s] = A_dd/len(years)        # average algae biomass production for 15 years (kg)
                
                G_dd_L = sum(G_kg_tot_den_L[:,s])
                G_kg_tot_dd_L[:,s] = G_dd_L/len(years)        # average grass biomass production for 15 years (kg)
                
                A_dd_L = sum(A_kg_tot_den_L[:,s])
                A_kg_tot_dd_L[:,s] = A_dd_L/len(years)        # average algae biomass production for 15 years (kg)
            
            
                
        CG_total = np.transpose(CG_kg_tot_dd)
        SB_total = np.transpose(SB_kg_tot_dd)
        G_total = np.transpose(G_kg_tot_dd)
        A_total = np.transpose(A_kg_tot_dd)
        G_total_L = np.transpose(G_kg_tot_dd_L)
        A_total_L = np.transpose(A_kg_tot_dd_L)
        
        Total = CG_total + SB_total + G_total + A_total + G_total_L + A_total_L
        CG_ethanol_total = np.zeros((len(solution),1))
        SB_oil_total = np.zeros((len(solution),1))
        G_energy_total = np.zeros((len(solution),1))
        A_energy_total = np.zeros((len(solution),1))
        G_energy_total_L = np.zeros((len(solution),1))
        A_energy_total_L = np.zeros((len(solution),1))
        Energy_total = np.zeros((len(solution),1))
        
        
        for s in solution:         
            
            GC_t = CG_total[s]   # corn yield kg/ha
            S_t = SB_total[s]   # soy yield kg/ha
            G_t = G_total[s]   # grass yield kg/ha
            A_t = A_total[s]   # algae yield kg/ha
            G_t_L = G_total_L[s]   # grass yield kg/ha
            A_t_L = A_total_L[s]   # algae yield kg/ha
        
            
            Energy =sum((9.42 * GC_t) + (8.02 * S_t) + (8.35* G_t) + (20.82* A_t) + (8.35* G_t_L) + (20.82*A_t_L))   # Ethanol * 29.7 MJ/kg + Soy Oil * 39.6 MJ/kg + biocrude * 21 MJ/kg + algae oil * 22 MJ/kg
            Energy_total[s] = Energy   # total energy MJ/yr
        
        
        df_O['MJ'] = Energy_total
        df_O['cost/MJ'] = df_O['cost']
        df_O['GHG_emission/MJ'] = df_O['GHG_emission']
 
        colors = df_O['MJ']
        
        x = df_O['cost/MJ']
        y = df_O['energy_shortfall']
        z = df_O['GHG_emission/MJ']
        
        plt.rcParams['font.sans-serif'] = "Arial"
        plt.rcParams["font.weight"] = "bold"
        plt.rcParams["axes.labelweight"] = "bold"
        
        plt.rcParams.update({'font.size': 14})
        
        fig, ax = plt.subplots(1,3, figsize=(13, 5.3),constrained_layout = True)
        fig.suptitle(b + v, fontsize=16)
        
        colorbar_min = min(Energy_total)
        colorbar_max = max(Energy_total)
        
        ### Cost/MJ vs Energy shortfall

        ax[0].scatter(x, y, c=colors, cmap='plasma');
        ax[0].tick_params(axis='both', which='major', labelsize=14)
        ax[0].set_xlabel('Cost ($/MJ)',fontsize=14)
        ax[0].set_ylabel('Quota Shortfall (MJ)',fontsize=14)

        axis_fontsize=14
        
        ax[0].grid(False)
        
        
        ### Cost/MJ vs GHG
        
        ax[1].scatter(x, z, c=colors, cmap='plasma');
        ax[1].tick_params(axis='both', which='major', labelsize=14)
        ax[1].set_xlabel('Cost ($/MJ)',fontsize=14)
        ax[1].set_ylabel(r'GHG Intensity (g $CO_{2}$ / MJ)',fontsize=14)

        axis_fontsize=14
        
        ax[1].grid(False)
        
        ### GHG emission/MJ vs Energy shortfall

        ax[2].scatter(z, y, c=colors, cmap='plasma');
        ax[2].tick_params(axis='both', which='major', labelsize=14)
        ax[2].set_xlabel(r'GHG Intensity (g $CO_{2}$ / MJ)',fontsize=14)
        ax[2].set_ylabel('Quota Shortfall (MJ)',fontsize=14)

        axis_fontsize=14
        
        ax[2].grid(False)
        ax[2].legend()

        
        cb_ax = fig.add_axes([1.05,.1,.015,0.8])
        fig.colorbar(mpl.cm.ScalarMappable(norm=mpl.colors.Normalize(vmin=colorbar_min, vmax=colorbar_max), cmap='plasma'),orientation='vertical',cax=cb_ax)
        cb_ax.set_ylabel('Energy Production (MJ)',fontsize=14, rotation=270, labelpad = 15)
        
        plt.savefig('Pareto_graph_district' + b + v + '.png',dpi=150, bbox_inches='tight')
    
    
    
