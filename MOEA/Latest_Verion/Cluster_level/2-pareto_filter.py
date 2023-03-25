# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import pandas as pd
import numpy as np

billion = ['3','6','9','12','15','18','20']

# billion = ['3']

version = ['district','_0.001district','_100000_0.1district','_100000_0.001district',
            '_1000000_0.1district','_1000000_0.001district','_10000000_0.1district','_10000000_0.001district']

# version = ['_0.001district']                                   


for b in billion:

    for v in version:
        
        fn = 'Results/Objective_functions_borg_crops_GHG' + b + v +'.csv'
        df_O = pd.read_csv(fn,header=0,index_col=0)
        
        
        fn_ha = 'Results/Decision_Variables_borg_crops_GHG' + b + v  +'.csv'
        df_D = pd.read_csv(fn_ha,header=0,index_col=0)
        
        
        P = []
        
        for i in range(0,len(df_O)):
            
            print(i)
            
            o1 = df_O.loc[i,'0']
            o2 = df_O.loc[i,'1']
            o3 = df_O.loc[i,'2']
            
            switch = 0
            
            for j in range(0,len(df_O)):
                
                if j == i:
                    
                    pass
                
                else:
                
                    s1 = df_O.loc[j,'0']
                    s2 = df_O.loc[j,'1']
                    s3 = df_O.loc[j,'2']
                    
                    if s1 < o1 and s2 < o2 and s3 < o3:
                    
                        switch = 1
            
            if switch < 1:
                
                P.append(i)
                
        df_O_filtered = df_O.loc[P]
        fn = 'Objective_functions_borg_crops_GHG' + b + v + '_PARETO' +'.csv'
        df_O_filtered.to_csv(fn)
        
                    
        
        df_D_filtered = df_D.loc[P]
        fn_ha = 'Decision_Variables_borg_crops_GHG' + b + v + '_PARETO' +'.csv'
        df_D_filtered.to_csv(fn_ha)