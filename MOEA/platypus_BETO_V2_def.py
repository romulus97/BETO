# -*- coding: utf-8 -*-
"""
Created on Wed Mar 24 09:52:17 2021

@author: tlpac
"""

from platypus import NSGAII, Problem, Real 
import random
from random import randint
import pandas as pd
import numpy as np
import time
import corn_stover_cultivation_V as CS_cultivation
import corn_stover_processing_V as CS_processing

def main(G, nc, nr, evl):
    start = time.time()

    #####################################################################
    ##########           IMPORT DATA           ##########################
    #####################################################################
    
    # import county level data
    df_geo = pd.read_excel('geodata_total.xlsx',header=0, engine='openpyxl')
    counties = list(df_geo['co_state'])
    
    #specify grouping
    groups = G
    
    #county-to-hub data
    filename = 'C2H_' + str(groups) + '.xlsx'
    df_C2H = pd.read_excel(filename,header=0, engine='openpyxl')
    c = list(df_C2H['co_state'])
    
    #eliminate and counties that don't appear in both lists
    for i in counties:
        idx = counties.index(i)
        if i in c:
            pass
        else:
            df_geo = df_geo.drop(index=idx)
    
    df_geo = df_geo.reset_index(drop=True)
    fips = df_geo['fips'].values
    counties = list(df_geo['co_state'])
    land_costs = df_geo.loc[:,'land_cost_dpa'].values # $ per acre
    land_limits = df_geo['land_limits_acre'].values # county ag production area in acres
    
    # Corn Stover
    bu_per_acre_C_yield = df_geo['yield_bpa'].values  #yield in bushels per acre
    
    
    ########################################################################
    #########        PRE-PROCESSING       ##################################
    ########################################################################
    
    ###################################
    # PROBLEM SIZE CONTROLS
    
    # Limit # of counties under consideration
    # put a number > 0 and < number of counties if desired; if not, problem defaults to full list of counties
    num_counties = nc
    
    reduced_counties = []
    reduced_land_costs = []
    reduced_land_limits = []
    reduced_C_yield = []
    
    if num_counties > 0:
        for i in range(0,num_counties):
            s = randint(0,len(counties)-1)
            if s in reduced_counties:
                pass
            else:
                reduced_counties.append(counties[s])
    else:
        reduced_counties = counties
        
    
        
    ################################
    # Convert to function inputs
    
    # Hub grouping information, distance look-up tables
    dist_C2H = []
    county_hubs = []
    for county in reduced_counties:
        
        idx = counties.index(county)
        
        reduced_land_costs.append(land_costs[idx])
        reduced_land_limits.append(land_limits[idx])
        reduced_C_yield.append(bu_per_acre_C_yield[idx])
        
        # distance from each county to pre-defined hub
        dist_C2H.append(df_C2H.loc[df_C2H['co_state']==county,'travel_dist_km'].values[0])
        
        # list of hubs assigned to each county
        county_hubs.append(df_C2H.loc[df_C2H['co_state']==county,'destinationID'].values[0])
    
    
    # Pre-define location of refineries
    # put a number > 0 and < number of hubs if desired; if not, problem defaults to full list of hubs
    num_refineries = nr
    
    #hub-to-hub data
    filename = 'H2H_' + str(groups) + '.xlsx'
    df_H2H = pd.read_excel(filename,header=0, engine='openpyxl')
    hubs = list(df_H2H['OriginID'].unique())
    
    locations = []
    
    if num_refineries > 0:
        for i in range(0,num_refineries):
            s = random.choice(hubs)
            if s in locations:
                pass
            else:
                locations.append(s)
    else:
        locations = hubs
        
    ################################
    # Convert to function inputs
    
    dist_map = np.zeros((len(hubs),len(locations)))
    
    # convert look-up table to distance matrix
    for i in range(0,len(hubs)):
        c1 = hubs[i]
        for j in locations: 
            c2 = j
            dist_map[i,locations.index(j)] = df_H2H.loc[(df_H2H['OriginID']==c1) & (df_H2H['DestinationID']==c2),'Total_Kilometers']
    
    map_C2H = np.zeros((len(reduced_counties),len(hubs)))
    
    # convert look-up table to distance matrix
    for i in range(0,len(reduced_counties)):
        h = hubs.index(int(county_hubs[i]))
        map_C2H[i,h] = 1    
    
    
    #########################################################
    # Identify quota as 50% of maximum theoretical production
    import determine_quota_V
    quota, UB = determine_quota_V.QD(groups,reduced_counties,locations)
    quota = quota[0]
    
        
    #####################################################################
    ##########           FUNCTION DEFINITION     ########################
    #####################################################################
       
    ###################################
    # CONVERSIONS
    ha_to_acre = 2.47105 # Hectares to Acres
    lb_to_kg= 0.453515 # pounds to kilograms
    kg_to_L_Ethanol = 1.273723
    
    # NOTE: MAKE SURE OF CONVERSIONS BELOW -- VALUES ABOVE NOW APPEAR ALL IN ACRES
        
        
    # simulation model (function to be evaluated by MOEA)
    def simulate(
        
        
            vars, # cultivation hectares per county, hub-to-hub biomass flows
            LC = reduced_land_costs, # land costs per county
            C_Y = reduced_C_yield, # corn yield per acre
            LL = reduced_land_limits, # land limits
            DM = dist_map, # hub to hub distances
            C2H_map = map_C2H, # binary matrix mapping counties (rows) to hubs (columns)
            C2H = dist_C2H, # county to hub distances
            locations = locations, #possible location of biorefineries,
            hubs = hubs,
            Q = quota
            
            ):
        
        # Empty parameters 
        CS_cultivation_capex = 0 
        CS_cultivation_opex = 0
        CS_travel_opex = 0
        CS_flow_matrix = np.zeros((len(hubs),len(locations)))
        CS_C2H_prod = np.zeros((len(LC),len(hubs)))
        CS_flow = 0
        CS_refinery_kg = 0
        CS_ethanol = np.zeros((len(locations),1))
        CS_refinery_capex = 0
        
        Constraints = [] # constraints
        
        # Per ha values (need to expand)
        (CS_per_ha, seeds_per_ha, fertilization_per_ha, lime_per_ha)  = CS_cultivation.sim(C_Y)
    
        # Capital costs (need to expand)
        L = np.array(LC)
        v = np.array(vars)
            
        CS_cultivation_capex = np.dot(v[0:len(LC)],L)
            
        ##############################
        # Cultivation and Harvesting
    
        # Operating costs (need to expand)
        harvesting = 38.31*ha_to_acre # $ per ha
        CS_cultivation_opex = np.dot(v[0:len(LC)],(seeds_per_ha*.00185 + fertilization_per_ha[0]*0.55 + fertilization_per_ha[1]*0.46 + fertilization_per_ha[2]*0.50 + lime_per_ha*0.01 + harvesting)) #herbicide in per ha??
        
        # Automatic flow to pre-processing hub
        CS_C2H_prod = C2H_map.dot(CS_per_ha.dot(v[0:len(LC)]))
    
        CS_cultivation_opex += sum(CS_per_ha*vars[0:len(LC)]*(lb_to_kg)*(1/1500)*0.50*C2H)
                    
        ################################
        #Flow to refinery
        ref = (len(LC) + (len(hubs) - 1)*len(locations) + (len(locations) - 1)) + 1
   
        # # Mass transfer (1Ms kg of CS) from hub 'j' to hub 'k'
        CS_flow_matrix = v[len(LC):ref].reshape((len(hubs),len(locations)))
    
        # Travel costs in bale-miles
        CS_travel_opex = np.sum(DM*CS_flow_matrix*((lb_to_kg)*(1/1500)*0.50)) 
    
        #for j in range(0,len(hubs)):
        P = np.array(CS_C2H_prod)
        F = np.array(CS_flow_matrix)
        
        # Hubs collect biomass from counties
        CS_hub_kg = np.sum(P, axis=0)
        
        # Transportation constraints (all delivery from hub 'j' must be <= mass produced)
        CS_flow = np.sum(F, axis=1)
        flow_constraints = CS_flow - CS_hub_kg - 5 #allow some slack in DVs
        
        for j in range(0,len(hubs)):
            
            Constraints.append(flow_constraints[j]) 
    
            
        ###############################
        # Refinery
       
        #for k in range(0,len(locations)):
              
        # Find total mass received at hub 'l'
        CS_refinery_kg = np.sum(F, axis=0)
                
        # Ethanol produced at refinery at hub 'l'
        CS_ethanol = CS_processing.sim(CS_refinery_kg)
        
        #for k in range(0,len(locations)):
            # Refinery capex
            #if CS_refinery_kg[k] > 5:   #skip or remove
        scale = CS_refinery_kg/(5563*142) # Based on kg per ha and ha scaling in Jack's TEA file
        CS_refinery_capex = 400000000*(scale)**.6
        
        # Sets ethanol production quota (L)
        Constraints.append(Q - np.sum(CS_ethanol))
        #Constraints.append(sum(CS_ethanol)[0] - Q*1.05) #remove upper contraint 
    
        Constraints = list(Constraints)
        
        # Returns list of objectives, Constraints
        return [sum(CS_refinery_capex), CS_travel_opex], Constraints
    
    
    #####################################################################
    ##########           MOEA EXECUTION          ########################
    #####################################################################
    
    # Number of variables, constraints, objectives
    g = len(reduced_land_costs)
    num_variables = g + len(hubs) * len(locations)
    num_constraints = len(hubs) + 1      #must match to contraints
    num_objs = 2
    
    problem = Problem(num_variables,num_objs,num_constraints)
    for i in range(0,len(reduced_land_costs)):
        problem.types[i] = Real(0,reduced_land_limits[i]+1)
    problem.types[g:] = Real(0,UB+1)
    problem.constraints[:] = "<=0"
    
    #What function?
    problem.function = simulate
    
    # What algorithm?
    algorithm = NSGAII(problem)
    
    # Evaluate function # of times
    algorithm.run(evl)
    
    stop = time.time()
    elapsed = (stop - start)/60
    mins = str(elapsed) + ' minutes'
    print(mins)
    
    
    #####################################################################
    ##########           OUTPUTS                 ########################
    #####################################################################
    
    solutions = [s for s in algorithm.result]
    
    D = np.zeros((len(solutions),num_variables))
    O = np.zeros((len(solutions),num_objs))
    
    for s in solutions:
        
        idx = solutions.index(s)
        # ax.scatter(s.objectives[0]/1000,s.objectives[1],s.objectives[2]*-1, c = 'red',alpha=0.5)
    
        #record solution information
        for i in range(0,num_variables):
            D[idx,i] = s.variables[i]
        for j in range(0,num_objs):
            O[idx,j] = s.objectives[j]
    
    df_D = pd.DataFrame(D)
    df_D.to_csv('Decision_Variables_all.csv')
    
    df_O = pd.DataFrame(O)
    df_O.to_csv('Objective_Functions_all.csv')
    
    
    # find constraints that are violated
    import constraint_test
    
    df = pd.read_csv('Decision_Variables_all.csv',header=0,index_col=0)
    
    LC = reduced_land_costs # land costs per county
    C_Y = reduced_C_yield # corn yield per acre
    LL = reduced_land_limits # land limits
    DM = dist_map # hub to hub distances
    C2H_map = map_C2H # binary matrix mapping counties (rows) to hubs (columns)
    C2H = dist_C2H # county to hub distances
    locations = locations #possible location of biorefineries,
    hubs = hubs
    Q = quota
    
    violations = {}
    
    for i in range(0,len(df)):
        DV = df.iloc[0,:] # take first solution
        [CS_refinery_capex, CS_travel_opex], Constraints = constraint_test.test(DV, LC, C_Y, LL, DM, C2H_map, C2H, locations, hubs, Q)
        C = []
        for j in range(0,len(Constraints)):
                if Constraints[j] > 0:
                    C.append(j)
        violations[i] = C
            
            
    
    # #limit evalutaion to 'feasible' solutions
    feasible_solutions = [s for s in algorithm.result if s.feasible]
    
    D = np.zeros((len(feasible_solutions),num_variables))
    O = np.zeros((len(feasible_solutions),num_objs))
    
    for s in feasible_solutions:
        
        idx = feasible_solutions.index(s)
        # ax.scatter(s.objectives[0]/1000,s.objectives[1],s.objectives[2]*-1, c = 'red',alpha=0.5)
    
        #record solution information
        for i in range(0,num_variables):
            D[idx,i] = s.variables[i]
        for j in range(0,num_objs):
            O[idx,j] = s.objectives[j]
    
    df_D = pd.DataFrame(D)
    df_D.to_csv('Decision_Variables.csv')
    
    df_O = pd.DataFrame(O)
    df_O.to_csv('Objective_Functions.csv')
    
    # obj1 = []
    # obj2 = []
    
    # for s in feasible_solutions:
    #     obj1.append(s.objectives[0])
    #     obj2.append(s.objectives[1])
        
    # min_obj1_idx = obj1.index(min(obj1))
    # min_obj2_idx = obj2.index(min(obj2))
    
    # # find solutions' standardized distance to ideal (origin)
    # distance_to_origin_pct = []
    
    # for s in feasible_solutions:
    #     d = ((s.objectives[0]/max(obj1))**2 + (s.objectives[1]/max(obj2))**2)**0.5
    #     distance_to_origin_pct.append(d)
    
        
    # # select range of standardized solutions to map
    # sorted_distance = np.sort(distance_to_origin_pct)
    # idx = []
    # idx_obj1 = []
    # for i in range(0,99,9):
    #     idx.append(distance_to_origin_pct.index(sorted_distance[i]))
    #     idx_obj1.append(obj1[i])
        
    # # display the tradeoff frontier    
    # import matplotlib.pyplot as plt
    
    # plt.scatter([s.objectives[0]/1000 for s in feasible_solutions],
    #             [s.objectives[1] for s in feasible_solutions],c='red',alpha=0.5)
    
    # plt.scatter(obj1[min_obj1_idx]/1000,obj2[min_obj1_idx],s=60,c='cyan',edgecolors='gray')
    # plt.scatter(obj1[min_obj2_idx]/1000,obj2[min_obj2_idx],s=60,c='cyan',edgecolors='gray')
    
    # for i in idx:
        
    #     plt.scatter(obj1[i]/1000,obj2[i],s=60,c='cyan',edgecolors='gray')
        
    # plt.xlabel("Costs ($1000s)")
    # plt.ylabel("Distance (km)")
    # plt.show()
    
    
    # # visualize (map) solutions
    # from urllib.request import urlopen
    # import json
    # with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
    #     counties = json.load(response)
    # import plotly.express as px
    # import plotly.io as pio
    # pio.renderers.default='jpg'
    
    # # plot in descending order from Obj1
    # df_combined = pd.DataFrame()
    # df_combined['idx'] = idx
    # df_combined['obj1'] = idx_obj1
    # df_sorted = df_combined.sort_values(by='obj1',ascending=False).reset_index(drop=True)
    
    
    # # map minimum obj1 solution
    # s = np.array(feasible_solutions[min_obj1_idx].variables)
    # df_results = pd.DataFrame()
    # df_results['fips'] = fips
    # df_results['CS_ha'] = s
    # df_results['fips'] = df_results['fips'].apply(str)
    # fig = px.choropleth(df_results, geojson=counties, locations='fips', color='CS_ha',
    #                            color_continuous_scale="Viridis",
    #                            range_color=(0, 50),
    #                            scope="usa",
    #                            labels={'CS_ha':'Corn Stover Hectares'}
    #                           )
    # fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    # fig.update_geos(fitbounds="locations", visible=False)
    # fig.show()
    
    # # map rest of selected solutions
    # for i in range(0,len(df_sorted)):
    #     j = df_sorted.loc[i,'idx']
    #     s = np.array(feasible_solutions[j].variables)
    #     df_results = pd.DataFrame()
    #     df_results['fips'] = fips
    #     df_results['CS_ha'] = s
    #     df_results['fips'] = df_results['fips'].apply(str)
    #     fig = px.choropleth(df_results, geojson=counties, locations='fips', color='CS_ha',
    #                                color_continuous_scale="Viridis",
    #                                range_color=(0, 50),
    #                                scope="usa",
    #                                labels={'CS_ha':'Corn Stover Hectares'}
    #                               )
    #     fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    #     fig.update_geos(fitbounds="locations", visible=False)
    #     fig.show()
    
    # # map minimum obj2 solution
    # s = np.array(feasible_solutions[min_obj2_idx].variables)
    # df_results = pd.DataFrame()
    # df_results['fips'] = fips
    # df_results['CS_ha'] = s
    # df_results['fips'] = df_results['fips'].apply(str)
    # fig = px.choropleth(df_results, geojson=counties, locations='fips', color='CS_ha',
    #                            color_continuous_scale="Viridis",
    #                            range_color=(0, 50),
    #                            scope="usa",
    #                            labels={'CS_ha':'Corn Stover Hectares'}
    #                           )
    # fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    # fig.update_geos(fitbounds="locations", visible=False)
    # fig.show()

