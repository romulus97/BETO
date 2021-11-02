# -*- coding: utf-8 -*-
"""
Created on Thu Oct 28 11:09:41 2021

@author: Ece Ari Akdemir
"""

import numpy as np
import pandas as pd

def sim(SB_refinery_kg):

    ##This code creates produced soybean oil as L for each year in each district. 
    ## In here total yield assumed that used for oil production. 
        
    # CONVERSIONS
    kg_ethanol_to_L_ethanol = 1.4 # kg soy oil to liters of soy oil
    soybean_oil = 1/(4.5)  # kg/kg Feedstock
    
    kg_soy_oil = SB_refinery_kg * soybean_oil

    L_soy_oil = kg_soy_oil * kg_ethanol_to_L_ethanol
    
    # gasoline_per_yr.append(gasoline_yr)
    
    # new_df_transpose = pd.DataFrame(np.transpose(L_ethanol),columns=df_corn.iloc[:,8:].columns)
    # df_new = df_corn.iloc[:,range(1,8)].copy()
    # df_new = pd.concat([df_new,new_df_transpose],axis=1)    
    # df_new.to_excel('yearly_ethanol.xlsx',index=False)
    return kg_soy_oil   