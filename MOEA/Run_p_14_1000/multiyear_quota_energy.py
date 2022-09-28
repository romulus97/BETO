# -*- coding: utf-8 -*-
"""
Created on Thu Oct 28 20:09:56 2021

@author: Ece Ari Akdemir
"""


import pandas as pd
import numpy as np
import corn_grain_processing as CG_processing
import soybean_processing as SB_processing 
import Pyrol_processing as G_processing 
import Algal_Oil as A_processing

def QD (districts,locations):

    #####################################################################
    ##########           IMPORT DATA           ##########################
    #####################################################################
    
    # import county level data
    df_geo = pd.read_excel('combined_pivot_corn_excel_electricity.xlsx',header=0, engine='openpyxl') #contains every eg_district code 
    df_geo_s = pd.read_excel('combined_pivot_soy_excel_electricity.xlsx',header=0, engine='openpyxl') #contains every eg_district code 
    df_geo_g = pd.read_excel('combined_pivot_grass_excel_electricity.xlsx',header=0, engine='openpyxl') #contains every eg_district code  
    df_geo_a = pd.read_excel('combined_pivot_algae_excel_electricity.xlsx',header=0, engine='openpyxl') #contains every eg_district code  
    
    districts = list(df_geo['STASD_N'])
    
    #specify grouping
    groups = 20
    
    #district-to-hub data
    filename = 'AgD2H_48_cb.csv'
    df_D2H = pd.read_csv(filename,header=0)
    c = list(df_D2H['STASD_N'])
    
    #eliminate districts that don't appear in both lists
    for i in districts:
        idx = districts.index(i)
        if i in c:
            pass
        else:
            df_geo = df_geo.drop(index=idx)
    
    df_geo = df_geo.reset_index(drop=True)
    # fips = df_geo['fips'].values
    districts = list(df_geo['STASD_N'])
    
    land_costs = df_geo.loc[:,'land_costs-$/ha'].values # $ per ha
    land_limits = df_geo['land_limits_ha'].values # county ag production area in acres
    
    marginal_land_costs = df_geo_g.loc[:,'land_costs-$/ha'].values # $ per ha
    marginal_land_limits = df_geo_g['land_limits_ha'].values # county ag production area in acres
    
    
    # # Corn Stover
    # C_yield = df_geo['yield_bpa'].values  #yield in bushels per acre
    C_yield = df_geo.loc[:,1998:2013].values
    S_yield = df_geo_s.loc[:,1998:2013].values
    G_yield = df_geo_g.loc[:,1998:2013].values
    A_yield = df_geo_a.loc[:,1998:2013].values  
    ########################################################################
    #########        PRE-PROCESSING       ##################################
    ########################################################################
    
    ################################
    # Convert to function inputs
    
    # Hub grouping information, distance look-up tables
    dist_D2H = []
    district_hubs = []
    for d in districts:
        
        # distance from each district to pre-defined hub
        dist_D2H.append(df_D2H.loc[df_D2H['STASD_N']==d,'travel_dist_km'].values[0])
        
        # list of hubs assigned to each county
        district_hubs.append(df_D2H.loc[df_D2H['STASD_N']==d,'destinationID'].values[0])
    
    
    #hub-to-hub data
    filename = 'AgD_48g_H2H_cb.csv'
    df_H2H = pd.read_csv(filename,header=0)
    hubs = list(df_H2H['OriginID'].unique())
    locations=hubs
        
    ################################
    # Convert to function inputs
    
    dist_map = np.zeros((len(hubs),len(locations)))
    
    # convert look-up table to distance matrix
    for i in range(0,len(hubs)):
        c1 = hubs[i]
        for j in range(0,len(locations)):
            c2 = locations[j]
            dist_map[i,j] = df_H2H.loc[(df_H2H['OriginID']==c1) & (df_H2H['DestinationID']==c2),'Total_Kilometers']
    
    map_D2H = np.zeros((len(districts), len(hubs)))
    
    # convert look-up table to distance matrix #when 50 is indexed 49 is not valid because of missing hubs
    for i in range(0,len(districts)):
        h = hubs.index(int(district_hubs[i])) # int(county_hubs[i]) - 1
        map_D2H[i,h] = 1    
                
    #####################################################################
    ##########           FUNCTION DEFINITION     ########################
    #####################################################################
       
    ###################################     
    #pre-load test decision variables
    V = []
    for a in range(0,len(districts)):
        V.append((land_limits[a])) 
      
    LC = land_costs # land costs per county
    
    V1 = []
    for a in range(0,len(districts)):
        V1.append((marginal_land_limits[a])) 
      
    
    D2H_map = map_D2H # binary matrix mapping counties (rows) to hubs (columns)
    locations = locations #possible location of biorefineries,
    hubs = hubs
    
    years = range(1998,2014)
    Q_series = []
    
    ##############################
    # Cultivation and Harvesting
    
    for b in years:
        
        
        # Empty parameters 
        CG_flow_matrix = np.zeros((len(hubs),len(locations)))
        CG_D2H_prod = np.zeros((len(LC),len(hubs)))
        CG_refinery_kg = 0
        CG_ethanol = np.zeros((len(locations),1))
            
        y = years.index(b)
        C_Y = C_yield[:,y]
        
        SB_flow_matrix = np.zeros((len(hubs),len(locations)))
        SB_D2H_prod = np.zeros((len(LC),len(hubs)))
        SB_refinery_kg = 0
        SB_oil = np.zeros((len(locations),1))
            
        y = years.index(b)
        S_Y = S_yield[:,y]
        
        G_flow_matrix = np.zeros((len(hubs),len(locations)))
        G_D2H_prod = np.zeros((len(LC),len(hubs)))
        G_refinery_kg = 0
        G_energy = np.zeros((len(locations),1))
            
        G_Y = G_yield[:,y]    
        
        A_flow_matrix = np.zeros((len(hubs),len(locations)))
        A_D2H_prod = np.zeros((len(LC),len(hubs)))
        A_refinery_kg = 0
        A_energy = np.zeros((len(locations),1))
            
        A_Y = A_yield[:,y]  
        
        for c in range(0,len(LC)):
    
            # Automatic flow to pre-processing hub
            CG_D2H_prod[c,:] = D2H_map[c,:]*C_Y[c]*(V[c]/2)
            SB_D2H_prod[c,:] = D2H_map[c,:]*S_Y[c]*(V[c]/2)
            G_D2H_prod[c,:] = D2H_map[c,:]*G_Y[c]*(V1[c])  
            A_D2H_prod[c,:] = D2H_map[c,:]*A_Y[c]*(V1[c])
    
            # # Automatic flow to pre-processing hub
            # d_index = districts.index(i)
            # CS_D2H_prod[d_index,:] = D2H_map[d_index,:]*C_Y[i]*V[i]
        
        ################################
            
        H2H_CG_flow = []
        H2H_SB_flow = []
        H2H_G_flow = []
        H2H_A_flow = []
        
        # Flow to refinery
        for d in range(0,len(hubs)):
            
            for e in range(0,len(locations)):
                
                H2H_CG_flow.append(sum(CG_D2H_prod[:,d])*(1/len(locations)))
            
                # Mass transfer (kg of CS) from hub 'j' to hub 'k'
                CG_flow_matrix[d,e] = CG_flow_matrix[d,e] + H2H_CG_flow[d*len(locations) + e]
                
                H2H_SB_flow.append(sum(SB_D2H_prod[:,d])*(1/len(locations)))
            
                # Mass transfer (kg of CS) from hub 'j' to hub 'k'
                SB_flow_matrix[d,e] = SB_flow_matrix[d,e] + H2H_SB_flow[d*len(locations) + e]
                
                H2H_G_flow.append(sum(G_D2H_prod[:,d])*(1/len(locations)))
            
                # Mass transfer (kg of CS) from hub 'j' to hub 'k'
                G_flow_matrix[d,e] = G_flow_matrix[d,e] + H2H_G_flow[d*len(locations) + e]
                
                H2H_A_flow.append(sum(A_D2H_prod[:,d])*(1/len(locations)))
            
                # Mass transfer (kg of CS) from hub 'j' to hub 'k'
                A_flow_matrix[d,e] = A_flow_matrix[d,e] + H2H_A_flow[d*len(locations) + e]
                    
            
        ###############################
        # Refinery #what it's doing is it's going through at each hub and figuring out how much biomass is delivered to each hub, and then it's sending that each refinery
        for k in range(0,len(locations)):
              
            # Find total mass received at hub 'l'
            CG_refinery_kg = sum(CG_flow_matrix[:,k])
            
            # Ethanol produced at refinery at hub 'l'
            CG_ethanol[k] = CG_processing.sim(CG_refinery_kg)
            
            # Find total mass received at hub 'l'
            SB_refinery_kg = sum(SB_flow_matrix[:,k])
            
            # Ethanol produced at refinery at hub 'l'
            SB_oil[k] = SB_processing.sim(SB_refinery_kg)
            
            # Find total mass received at hub 'l'
            G_refinery_kg = sum(G_flow_matrix[:,k])
            
            # Ethanol produced at refinery at hub 'l'
            G_energy[k] = G_processing.sim(G_refinery_kg)
            
            A_refinery_kg = sum(A_flow_matrix[:,k])
            
            # Ethanol produced at refinery at hub 'l'
            A_energy[k] = A_processing.sim(A_refinery_kg)
    
        
        Energy_corn = ( 29.7 * CG_ethanol + 39.6 * SB_oil + 21 * G_energy + 22 * A_energy)    # Ethanol * 29.7 MJ/kg + Soy Oil * 39.6 MJ/kg + biocrude * 21 MJ/kg + algae oil * 22 MJ/kg
        
        s = sum(Energy_corn[:])
        # Q.append(s[0])
        Q_series.append(s[0]) #total corn grain kg 
        Q_min = min(Q_series)

    return Q_min,Q_series 
