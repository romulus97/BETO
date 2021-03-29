# -*- coding: utf-8 -*-
"""
Created on Wed Mar 24 10:09:11 2021

@author: tlpac
"""
import os
import time
import shutil
import platypus_BETO_V_def

start = time.time()

groups = 20
counties = 20
refineries = 1
evolutions = 100000

G = groups
nc = counties
nr = refineries
# evl = evolutions

for i in range(1, 11): 
    
    evl = i * 100000
    
    platypus_BETO_V_def.main(G, nc, nr, evl)
    
    filename = '\Decision_Variables_' + str(G) + str(nc) + str(nr) + '_' + str(i + 1) + '.csv'
    destination = 'D:\KernInternship\BETO\MOEA\Outputs\Time_test_generations' + filename
    os.rename(r'D:\KernInternship\BETO\MOEA\Decision_Variables.csv', r'D:\KernInternship\BETO\MOEA' + filename)
    shutil.move('D:\KernInternship\BETO\MOEA' + filename, destination)
    
    filename2 = '\Decision_Variables_all_' + str(G) + str(nc) + str(nr) + '_' + str(i + 1) + '.csv'
    destination2 = 'D:\KernInternship\BETO\MOEA\Outputs\Time_test_generations' + filename2
    os.rename(r'D:\KernInternship\BETO\MOEA\Decision_Variables_all.csv', r'D:\KernInternship\BETO\MOEA' + filename2)
    shutil.move('D:\KernInternship\BETO\MOEA' + filename2, destination2)
    
    filename3 = '\Objective_Functions_' + str(G) + str(nc) + str(nr) + '_' + str(i + 1) + '.csv'
    destination3 = 'D:\KernInternship\BETO\MOEA\Outputs\Time_test_generations' + filename3
    os.rename(r'D:\KernInternship\BETO\MOEA\Objective_Functions.csv', r'D:\KernInternship\BETO\MOEA' + filename3)
    shutil.move('D:\KernInternship\BETO\MOEA' + filename3, destination3)
    
    filename4 = '\Objective_Functions_all_' + str(G) + str(nc) + str(nr) + '_' + str(i + 1) + '.csv'
    destination4 = 'D:\KernInternship\BETO\MOEA\Outputs\Time_test_generations' + filename4
    os.rename(r'D:\KernInternship\BETO\MOEA\Objective_Functions_all.csv', r'D:\KernInternship\BETO\MOEA' + filename4)
    shutil.move('D:\KernInternship\BETO\MOEA' + filename4, destination4)

stop = time.time()
elapsed = (stop - start)/60
mins = str(elapsed) + ' minutes'
print(mins)