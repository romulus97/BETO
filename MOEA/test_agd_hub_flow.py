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
import corn_stover_cultivation_V as CS_cultivation
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

geodata = pd.read_excel('agd_geodata_cb.xlsx', engine='openpyxl')

######################################################
################## PROCESSING ########################
######################################################

num_refineries = 0 #Set number of refineries

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

hub_dist[r_idx] = 0 #hubs that are choosen go to stay don't transfer

df_hub_dist = pd.DataFrame(hub_dist) #dataframe of hub_dist

hub_flow = np.argmin(np.where(flow_map==0, flow_map.max(), flow_map), axis=1) #index of closest refinery to hub   

hub_flow[r_idx] = r_idx #hubs that are choosen don't transfer

if num_refineries == 1: #argmin messes up at 1 refinery but this fixes it
    hub_flow[np.where(hub_flow == 0)] = r_idx
else:
    pass


    
C_Y = np.array(geodata['yield_bpa'])

(CS_per_ha, seeds_per_ha, fertilization_per_ha, lime_per_ha)  = CS_cultivation.sim(C_Y)

CS_per_ha_list = CS_per_ha.tolist()

r = randint(0,99) #chose random cultivation decisions from file

AgD_hec = AgD_cultivation[r:(r+1)].T #pull cultivation and transpose into column

AgD_hec['CS_per_ha'] = CS_per_ha_list

AgD_hec['kg'] = AgD_hec[r] * AgD_hec['CS_per_ha']

AgD_c = AgD_hec['kg'].reset_index()

AgD_c['hub'] = AgD2H['destinationID'] #add list of closest hubs

h_c_sum = AgD_c.groupby(['hub']).agg({'kg': sum}).reset_index() #amount of cultivation that is at each hub  

hub_sum = h_c_sum.drop(columns=['hub']) #drop hub column



truck_load = pd.DataFrame(np.array(hub_sum)/14969) #amount a truck can carry in kg (abitrary value. looked up on wiki)

travel_costs = truck_load * ((np.array(df_hub_dist)/1.609) * 2.00) #total travel cost of all biomass from hub to closest refinery (does not include truck return trip and approximating $2 per mi)

travel_costs_total = np.sum(np.array(travel_costs)) #total transportation costs



h_c_sum['refinery'] = hub_flow #add refinery destination

ref_sum = h_c_sum.groupby(['refinery']).agg({'kg': sum}).reset_index() #sum culivation at refinery
                                                
ref_kg = np.array(ref_sum.drop(columns=['refinery'])) #drop refinery column

ref = (np.array(ref_sum.drop(columns='kg')) + 1 ) #refinery index list to refinery number

scale = ref_kg/(5563*142) # Based on kg per ha and ha scaling in Jack's TEA file

refinery_capex = 400000000*((scale)**.6) #Jack's scale 



ref_costs = pd.DataFrame(refinery_capex) #convert to df

ref_costs_total = np.sum(np.array(ref_costs)) #total refinery costs

ref_costs['refinery'] = ref #add refinery number to ref_costs

travel_costs['refinery'] = (np.array(h_c_sum['refinery']) + 1) #refinery index to refinery number add to travel costs

######################################################
##################### RESULTS ########################
######################################################

print(travel_costs) # $
    
print(travel_costs_total) # $

print(ref_costs)  # $

print(ref_costs_total) # $

print(r_loc)
  
stop = time.time()
elapsed = (stop - start)/60
mins = str(elapsed) + ' minutes'
print(mins)