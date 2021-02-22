"""
Created on Fri Jul  3 16:20:20 2020

@author: jkern
"""
import pandas as pd
import numpy as np
import corn_stover_cultivation as CS_cultivation
import corn_stover_processing as CS_processing


def QD (groups,reduced_counties,locations):

    #####################################################################
    ##########           IMPORT DATA           ##########################
    #####################################################################
    
    # import county level data
    df_geo = pd.read_excel('geodata_total.xlsx',header=0)
    counties = list(df_geo['co_state'])
    
    #county-to-hub data
    filename = 'C2H_' + str(groups) + '.xlsx'
    df_C2H = pd.read_excel(filename,header=0)
    c = list(df_C2H['co_state'])
    
    #eliminate and counties that don't appear in both lists
    for i in counties:
        idx = counties.index(i)
        if i in c:
            pass
        else:
            df_geo = df_geo.drop(index=idx)
    
    df_geo = df_geo.reset_index(drop=True)
    counties = list(df_geo['co_state'])
    land_costs = df_geo.loc[:,'land_cost_dpa'].values # $ per acre
    land_limits = df_geo['land_limits_acre'].values # county ag production area in acres
    
    # Corn Stover
    bu_per_acre_C_yield = df_geo['yield_bpa'].values  #yield in bushels per acre
        
    ################################
    # Convert to function inputs
    
    reduced_land_costs = []
    reduced_land_limits = []
    reduced_C_yield = []
    
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
    
    
    #hub-to-hub data
    filename = 'H2H_' + str(groups) + '.xlsx'
    df_H2H = pd.read_excel(filename,header=0)
    hubs = list(df_H2H['OriginID'].unique())
    
           
    ################################
    # Convert to function inputs
    
    dist_map = np.zeros((len(hubs),len(locations)))
    
    # convert look-up table to distance matrix
    for i in range(0,len(hubs)):
        c1 = hubs[i]
        for j in range(0,len(locations)):
            c2 = hubs[locations[j]-1]
            dist_map[i,j] = df_H2H.loc[(df_H2H['OriginID']==c1) & (df_H2H['DestinationID']==c2),'Total_Kilometers']
    
    map_C2H = np.zeros((len(reduced_counties),len(hubs)))
    
    # convert look-up table to distance matrix
    for i in range(0,len(reduced_counties)):
        h = int(county_hubs[i]) - 1
        map_C2H[i,h] = 1    
            
    #####################################################################
    ##########           FUNCTION DEFINITION     ########################
    #####################################################################
       
    ###################################
    #pre-load test decision variables
    V = []
    for i in range(0,len(reduced_counties)):
        V.append(reduced_land_limits[i]*0.50) #50% of theoretical capacity
      
    LC = reduced_land_costs # land costs per county
    C_Y = reduced_C_yield # corn yield per acre
    C2H_map = map_C2H # binary matrix mapping counties (rows) to hubs (columns)
    locations = locations #possible location of biorefineries,
    hubs = hubs
    
    # Empty parameters 
    CS_flow_matrix = np.zeros((len(hubs),len(locations)))
    CS_C2H_prod = np.zeros((len(LC),len(hubs)))
    CS_refinery_kg = 0
    CS_ethanol = np.zeros((len(locations),1))

    
    ##############################
    # Cultivation and Harvesting
        
    for i in range(0,len(LC)):
        
        # Per ha values (need to expand)
        (CS_per_ha, seeds_per_ha, fertilization_per_ha, lime_per_ha)  = CS_cultivation.sim(C_Y[i])
              
        # Automatic flow to pre-processing hub
        CS_C2H_prod[i,:] = C2H_map[i,:]*CS_per_ha*V[i]
    
    ################################
        
    # Flow to refinery
    for j in range(0,len(hubs)):
        
        for k in range(0,len(locations)):
            
            V.append(sum(CS_C2H_prod[:,j])*(1/len(locations)))
        
            # Mass transfer (kg of CS) from hub 'j' to hub 'k'
            CS_flow_matrix[j,k] = CS_flow_matrix[j,k] + V[i + 1 + j*len(locations) + k]
                
        
    ###############################
    # Refinery
    for k in range(0,len(locations)):
          
        # Find total mass received at hub 'l'
        CS_refinery_kg = sum(CS_flow_matrix[:,k])
        
        # Ethanol produced at refinery at hub 'l'
        CS_ethanol[k] = CS_processing.sim(CS_refinery_kg)
    
    ###############################
    # Upper bound hub 1Ms kgs
    UB = 0
    for j in range(0,len(hubs)):
        UB = max(UB,sum(CS_C2H_prod[:,j]))

    return [sum(CS_ethanol[:]),UB]

