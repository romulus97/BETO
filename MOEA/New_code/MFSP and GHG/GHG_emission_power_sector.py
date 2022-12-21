# -*- coding: utf-8 -*-
"""
Created on Mon Sep 19 20:11:07 2022

@author: eari
"""

import pandas as pd
import numpy as np
from scipy.interpolate import interp1d

# crops
crops = ['AlgaePLC','AlgaeMLC','CornPLC','SoyPLC','SwitchPLC','SwitchMLC']

crops2 = ['land_algae','algae','corn','soy','land_grass','grass']

years = range(1998,2014)

for c in crops:
    
    idx = crops.index(c)
    
    name = c
    name2 = 'combined_pivot_' + crops2[idx] + '_excel_electricity.xlsx' 

    # import lookup table from Jack
    df = pd.read_excel('Final_Lookup_Output_GHG.xlsx',sheet_name= name, header=0)
    gas_emission = df.iloc[:,3:]
    
    categories = gas_emission.columns.values
    # import data from Ece
    df2 = pd.read_excel(name2,header=0,index_col=0)
    districts = list(df2['STASD_N'])
    
    sample = df2.loc[:,1998:2013]
    
    shape = np.shape(sample)
    GHGs = np.zeros(shape)
    
    for i in range(0,shape[0]):
        
        for j in range(0,shape[1]):
            
            element = sample.iloc[i,j]
            
            for z in range(0,len(categories)-1):
                
                selected_bound = categories[[z,z+1]]
                lower_bound = selected_bound[0]
                upper_bound = selected_bound[1]
                
                if (element>lower_bound) and (element<upper_bound):
                    
                    selected_data = gas_emission.loc[i,selected_bound]
                    
                    x = [lower_bound,upper_bound]
                    y = [selected_data.values[0],selected_data.values[1]]
                    interpolate_func = interp1d(x, y, kind='linear')
                    new_prediction = float(interpolate_func(element))
                    GHGs[i,j] = new_prediction
                    
                else:
                    pass
    
    final_data = pd.DataFrame(GHGs, columns=years)        

    if c == 'AlgaePLC':
        final_data.to_excel('Algae_L_GHG_power_sector.xlsx',index=False)
        
    elif c == 'AlgaeMLC':
        final_data.to_excel('Algae_GHG_power_sector.xlsx',index=False)
    
    elif c == 'CornPLC':
        final_data.to_excel('Corn_GHG_power_sector.xlsx',index=False)
    
    elif c == 'SoyPLC':
        final_data.to_excel('Soy_GHG_power_sector.xlsx',index=False)
        
    elif c == 'SwitchPLC':
        final_data.to_excel('Switchgrass_L_GHG_power_sector.xlsx',index=False)
        
    elif c == 'SwitchMLC':
        final_data.to_excel('Switchgrass_GHG_power_sector.xlsx',index=False)
        

        
            
            
            
            
            
            
    