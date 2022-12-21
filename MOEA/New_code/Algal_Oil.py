# -*- coding: utf-8 -*-
"""
Created on Mon Jan 10 21:32:35 2022

@author: Ece Ari Akdemir
"""

import numpy as np
import pandas as pd

def sim(A_refinery_kg):

    ##This code creates produced soybean oil as L for each year in each district. 
    ## In here total yield assumed that used for oil production. 
        
    # CONVERSIONS
    Algal_oil = 0.5 # kg/kg Feedstock
    
    kg_algal_oil = A_refinery_kg * Algal_oil

    
    # gasoline_per_yr.append(gasoline_yr)
    
    # new_df_transpose = pd.DataFrame(np.transpose(L_ethanol),columns=df_corn.iloc[:,8:].columns)
    # df_new = df_corn.iloc[:,range(1,8)].copy()
    # df_new = pd.concat([df_new,new_df_transpose],axis=1)    
    # df_new.to_excel('yearly_ethanol.xlsx',index=False)
    return kg_algal_oil   