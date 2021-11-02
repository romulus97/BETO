
"""
Created on Fri Jul  3 16:20:20 2020

@author: jkern
"""

import numpy as np
import pandas as pd

def sim(CG_refinery_kg):

    ##This code creates produced ethano as liter for each year in each district. 
    ## In here total yield assumed that used for ethanol production. 
    # df_StarchFerm = pd.read_excel('CSU_All_Pathway_TEALCA_091621.xlsx', sheet_name ='StarchFerm', header=0)
    # df_corn =  pd.read_excel('combined_pivot_excel_electricity.xlsx', header=0)
        
    # CONVERSIONS
    kg_ethanol_to_L_ethanol = 1.267427123 # kg ethanol to liters of ethanol
    ethanol_to_biomass = 0.317040333  # df_StarchFerm.iloc[16:17,1:2].values[0][0] # kg of ethanol to kg of corn grain biomass
    gasoline = 0.014532693  # df_StarchFerm.iloc[8:9,1:2].values[0][0] # kg per kg corn grain
    
    
    # Corn Grain yield
    # C_yield = df_corn.iloc[:,8:].values  #yield in bushels per acre 
    # CG_Yield = C_yield
    
    # land_limit = df_corn['land_limits_ha'].values
    
    # gasoline_per_yr = []
        
    gasoline_yr = CG_refinery_kg * gasoline
        
    kg_ethanol = gasoline_yr + CG_refinery_kg * ethanol_to_biomass 

    L_ethanol = kg_ethanol * kg_ethanol_to_L_ethanol
    
    # gasoline_per_yr.append(gasoline_yr)
    
    # new_df_transpose = pd.DataFrame(np.transpose(L_ethanol),columns=df_corn.iloc[:,8:].columns)
    # df_new = df_corn.iloc[:,range(1,8)].copy()
    # df_new = pd.concat([df_new,new_df_transpose],axis=1)    
    # df_new.to_excel('yearly_ethanol.xlsx',index=False)
    return L_ethanol   
    
    
    
    
    
    
    
    
    
    
    
