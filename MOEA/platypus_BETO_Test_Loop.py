# -*- coding: utf-8 -*-
"""
Created on Fri Mar 12 09:33:43 2021

@author: tlpack
"""

import os
import shutil
import time
import platypus_BETO_def

start = time.time()

group = 20 
counties = 20 
hubs = 1

for i in range(0,25):
    
    platypus_BETO_def.main()
    
    filename = '\Decision_Variables_' + str(group) + str(counties) + str(hubs) + '_' + str(i + 1) + '.csv'
    destination = 'D:\KernInternship\BETO\MOEA\Outputs\Decision_Variables' + filename
    os.rename(r'D:\KernInternship\BETO\MOEA\Decision_Variables.csv', r'D:\KernInternship\BETO\MOEA' + filename)
    shutil.move('D:\KernInternship\BETO\MOEA' + filename, destination)
    
    filename2 = '\Decision_Variables_all_' + str(group) + str(counties) + str(hubs) + '_' + str(i + 1) + '.csv'
    destination2 = 'D:\KernInternship\BETO\MOEA\Outputs\Decision_Variables' + filename2
    os.rename(r'D:\KernInternship\BETO\MOEA\Decision_Variables_all.csv', r'D:\KernInternship\BETO\MOEA' + filename2)
    shutil.move('D:\KernInternship\BETO\MOEA' + filename2, destination2)
    
    filename3 = '\Objective_Functions_' + str(group) + str(counties) + str(hubs) + '_' + str(i + 1) + '.csv'
    destination3 = 'D:\KernInternship\BETO\MOEA\Outputs\Objective_Functions' + filename3
    os.rename(r'D:\KernInternship\BETO\MOEA\Objective_Functions.csv', r'D:\KernInternship\BETO\MOEA' + filename3)
    shutil.move('D:\KernInternship\BETO\MOEA' + filename3, destination3)
    
    filename4 = '\Objective_Functions_all_' + str(group) + str(counties) + str(hubs) + '_' + str(i + 1) + '.csv'
    destination4 = 'D:\KernInternship\BETO\MOEA\Outputs\Objective_Functions' + filename4
    os.rename(r'D:\KernInternship\BETO\MOEA\Objective_Functions_all.csv', r'D:\KernInternship\BETO\MOEA' + filename4)
    shutil.move('D:\KernInternship\BETO\MOEA' + filename4, destination4)


stop = time.time()
elapsed = (stop - start)/60
mins = str(elapsed) + ' minutes'
print(mins)

