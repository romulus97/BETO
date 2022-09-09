# -*- coding: utf-8 -*-
"""
Created on Fri Sep  9 10:37:32 2022

@author: jkern
"""

import pandas as pd
import numpy as np



# crops
crops = ['Algae','Corn','Soy','Switchgrass']

crops2 = ['algae','corn','soy','switchgrass']

for c in crops:
    
    idx = crops.index(c)
    
    name = c + ' Lookup'
    name2 = 'combined_pivot_' + crops2[idx] + '_excel_electricity.xlsx' 

    # import lookup table from Jack
    df = pd.read_excel('Final Output Table.xlsx',sheet_name= name, header=0)
    
    # import data from Ece
    df2 = pd.read_excel(name2,header=0,index_col=0)
    
    sample = df2.loc[:,1998:2013]
    
    shape = np.shape(sample)
    GHGs = np.zeros(shape)
    MFSP = np.zeros(shape)
    
    yield_range = df.columns[3:]
    
    for i in range(shape[0]):
        
        for j in range(shape[1]):
            
            element = sample.iloc[i,j]
            
            # test1 = element > yield_range
            # test2 = element < yield_range
            
            
            
    
    