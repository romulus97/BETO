# -*- coding: utf-8 -*-
"""
Created on Mon Sep 19 20:11:07 2022

@author: eari
"""

import pandas as pd
import numpy as np
from scipy.interpolate import interp1d

# crops
crops = ['AlgaeNLC','CornNLC','SoyNLC','SwitchNLC']

crops2 = ['algae','corn','soy','grass']

years = range(1998,2014)

for c in crops:
    
    idx = crops.index(c)
    
    name = c 
    name2 = 'combined_pivot_' + crops2[idx] + '_excel_electricity.xlsx' 

    # import lookup table from Jack
    df = pd.read_excel('Final_Lookup_Output_MFSP.xlsx',sheet_name= name, header=0)
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
    
    if c == 'AlgaeNLC':
        final_data.to_excel('Algae_MFSP.xlsx',index=False)

    elif c == 'CornNLC':
        final_data.to_excel('Corn_MFSP.xlsx',index=False)
    
    elif c == 'SoyNLC':
        final_data.to_excel('Soy_MFSP.xlsx',index=False)
        
    elif c == 'SwitchNLC':
        final_data.to_excel('Switchgrass_MFSP.xlsx',index=False)
        
        
            
            
            
            
            
            
    