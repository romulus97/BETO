# -*- coding: utf-8 -*-
"""
Created on Tue May 18 18:05:37 2021

@author: tlpac
"""

#from platypus import NSGAII, Problem, Real
import random
from random import randint
import pandas as pd
import numpy as np
import time
#import corn_stover_cultivation_V as CS_cultivation
#import corn_stover_processing_V as CS_processing

start = time.time()
version = 'scale_filter_district'

######################################################
################## IMPORT DATA #######################
######################################################

AgD_cultivation = pd.read_csv('Decision_Variables_' + version + '.csv', index_col=0)

AgD2H = pd.read_excel('AgD2H_48_cb.xlsx', engine='openpyxl')

H2H = pd.read_excel('AgD_48g_H2H_cb.xlsx', engine='openpyxl')

cords = pd.read_csv('AgD_48g_cords_cb.csv')

hubs = cords['Hubs'].to_list()

######################################################
################## PROCESSING ########################
######################################################

num_refineries = 3 #Set number of refineries

r_loc = [] #refineries chosen

if num_refineries > 0: #choose a random hub to be a refinery
    for i in range(0,num_refineries):
        s = random.choice([x for x in hubs if x not in r_loc])
        if s in r_loc:
            pass
        else:
            r_loc.append(s)
else:
    r_loc = hubs

H2H_map = np.zeros((len(hubs), len(hubs))) #map of H2H distances

for i in hubs: #plot to matrix
    for j in hubs: 
       H2H_map[(i-1),(j-1)] = H2H.loc[(H2H['OriginID']==i) & (H2H['DestinationID']==j),'Total_Kilometers']

r_idx = np.array(r_loc) - 1 #indexes for hubs

r_map = H2H_map[:,[r_idx]] #only distances from each hub to each refinery

flow_map = np.zeros((len(hubs), len(hubs))) #full matrix for hub to refinery  

flow_map[:,[r_idx]] = r_map # '' #

hub_dist = np.min(np.where(flow_map==0, flow_map.max(), flow_map), axis=1) #distance from each hub to closest refinery

df_hub_dist = pd.DataFrame(hub_dist) #dataframe of hub_dist

hub_flow = np.argmin(np.where(flow_map==0, flow_map.max(), flow_map), axis=1) #index of closest refinery to hub   

AgD2H_flow = AgD2H['destinationID'].to_list() #list from each AgD to closest hub

r = randint(0,99) #chose random cultivation decisions from file

AgD_hec = AgD_cultivation[r:(r+1)].T #pull cultivation and transpose into column

AgD_c = pd.DataFrame(np.array(AgD_hec) * 12553) #covert to kg (abitrary value. approx. 200 bu/acre)

AgD_c['hub'] = AgD2H_flow #add list of closest hubs

h_c_sum = AgD_c.groupby(['hub']).agg({0: sum}).reset_index() #amount of cultivation that is at each hub  

hub_sum = h_c_sum.drop(columns=['hub']) #drop hub column

truck_load = pd.DataFrame(np.array(hub_sum)/14969) #amount a truck can carry in kg (abitrary value. looked up on wiki)

travel_costs = truck_load * df_hub_dist #total travel cost of all biomass from hub to closest refinery (does not include truck return trip)

h_c_sum['refinery'] = hub_flow #add refinery destination

ref_sum = h_c_sum.groupby(['refinery']).agg({0: sum}).reset_index() #sum culivation at refinery
                                                
ref_kg = np.array(ref_sum.drop(columns=['refinery'])) #drop refinery column

ref = (np.array(ref_sum.drop(columns=[0])) + 1 ) #refinery index list to refinery number

scale = ref_kg/(5563*142) # Based on kg per ha and ha scaling in Jack's TEA file

refinery_capex = 400000000*((scale)**.6) #Jack's scale 

ref_costs = pd.DataFrame(refinery_capex) #convert to df

ref_costs['refinery'] = ref #add refinery number to ref_costs

travel_costs['refinery'] = (np.array(h_c_sum['refinery']) + 1) #refinery index to refinery number add to travel costs

######################################################
##################### RESULTS ########################
######################################################

print(travel_costs) # $
    
print(ref_costs)  # $
   
  
stop = time.time()
elapsed = (stop - start)/60
mins = str(elapsed) + ' minutes'
print(mins)