
"""
Created on Fri Jul  3 16:20:20 2020

@author: jkern
"""

import numpy as np
import pandas as pd
import Agriculture
import Process

def csp(F,R):
    
    ###################################
    # CONVERSIONS
    ha_to_acre = 2.47105 # Hectares to Acres
    gal_to_acre_feet = 3.07e-6 # Gallons to Acre-feet
    lb_to_kg= 0.453515 # pounds to kilograms
    Bushels_corn_to_kg = 25.4
    Miles_to_km = 1.60934
    kWh_to_MJ = 3.6
    gal_to_L = 3.78541
    kg_to_ton = 0.00110231
    ton_to_bu = 35.71428571
    
    
    ###################################
    # INPUTS
    bu_per_acre = 175 # Bushels Corn per Acre
    seeds_per_acre = 3000 # Seeds per Acre
    seeds_per_ha = seeds_per_acre*ha_to_acre # Seeds per Hectare
    fertilizer_per_acre = np.array([144, 64, 82]) # lb N , P2O5 , K2O per acre
    Lime_tretment = 183.04 # kg of lime per acre
    Herbicide_Atrazibe = 1.082 #lb of Atrezine per acre 
    hours_per_ha_laber = 2.965
    L_diesel_per_ha = 56.124
    
    field_to_biorefinary = 10 # miles
    Truck_Capacity = 20 #tonnes
    
    Comminution_energy = 0.1404 # MJ per kg stover
    Percent_to_hammer_mill = 97 # percent of corn stover goes into hammer mill is comminuted 
    
    ###################################
    # AGRICULTURE 100s
    
    #110 - Land dedication and seeding
    arable_land = 1 #ha
    seeded_land = Agriculture.LDS(arable_land) # Seeded land in hectares
    
    #120 - Irrigation
    h2o_per_acre = Agriculture.Irr(bu_per_acre) # H2O per acre
    gals_h2o_per_acre = h2o_per_acre*27154 # 
    gals_h2o_per_ha = gals_h2o_per_acre*ha_to_acre
    
    #130 - Fertilizers (N, P, K)
    fert_per_ha = fertilizer_per_acre * lb_to_kg * ha_to_acre # Converting the fertilization requirment from lb/acre to kg/ha
    fertilizer_per_ha = Agriculture.Frt (fert_per_ha, arable_land) # Total fertilizer required for the arable lands
    
    #140 - Soil pH managment
    Lime_per_ha = Lime_tretment * ha_to_acre
    
    #160 - Herbicide 
    Herbicide_per_ha = Herbicide_Atrazibe * ha_to_acre * lb_to_kg
    
    #170 - Crop Operations
    Laber_h_per_ha = hours_per_ha_laber
    L_deisel= L_diesel_per_ha
    
    #180 - Harvest Yeild 
    kg_corn_grain_per_ha = bu_per_acre * Bushels_corn_to_kg * ha_to_acre
    corn_stover_per_ha = kg_corn_grain_per_ha * 0.8867
    kg_stover_per_ha = Agriculture.Stover(corn_stover_per_ha, arable_land)
    
    #190 - Storage and Transportation
    transportation = field_to_biorefinary * Miles_to_km #km
    num_of_trucks = Agriculture.TRK (kg_stover_per_ha, Truck_Capacity)
    
    ###################################
    
    # BIOPROCESS NAD CONVERSION 200 - 600
     
    # 200 - Size Reduction Process - Comminution 
    comm = Process.COMM (kg_stover_per_ha , Comminution_energy , Percent_to_hammer_mill)
    Comminution_Electricity = comm [1] #MJ/ha
    kg_comm_stover_ha = comm [0] # kg comminuted stover per ha
    
    # 300 - Dilute acid hydrolysis 
    
    # Yeild & Conversions:
    Matrl_Handling_Energy = 241.79 # MJ/ha
    water_to_stover_ratio = 4
    acid_purity = 8 # acide weight percent (%)
    H2SO4 = 98.079 # H2SO4 molar mass
    NH3 = 17.031 # NH3 molar mass
    Cp_water = 4.184 # water heat capacity kJ/kg C
    Cp_stover = 1.03 # Stover heat capacity kJ/kg C 
    Cp_H2SO4 = 1.34 # H2SO4 heat capacity kJ/kg C
    final_temp = 175 # degree C
    int_temp = 20 # degree C 
    temp_diff =final_temp - int_temp # Temprture difference that the mixture should be heated (degree C)
    
    # Conversion rates:
    Cellulose = 0.4105
    Cellulose_to_Glucose = 81.3 # %
    Hemicellulose_to_Xylose = 67 # %
    Total_Mass_Conv = 97.3 # %
    
    dah = Process.DAH (kg_comm_stover_ha , water_to_stover_ratio , acid_purity , NH3 , 
             H2SO4 , Cp_water , Cp_stover , Cp_H2SO4 ,temp_diff , Total_Mass_Conv )
    
    Heating_energy = dah[0]
    kg_PreHydrolysate_Slurry_per_ha = dah[1]
    kg_Stover_PostDAH_per_ha = dah[2]
    
    # 400 - Enzymatic Hydrolysis
    #Conversions and Yield
    Water_to_Prehydrolysate = 4 # Ratio
    Cellulase_to_Cellulose = 0.02 # Ratio
    slurry_int_temp = 175 # dgree C
    slurry_final_temp = 48 # degree C
    slurry_temp_diff = slurry_int_temp - slurry_final_temp
    
    eh = Process.EH (kg_Stover_PostDAH_per_ha , water_to_stover_ratio , Cellulase_to_Cellulose , Cp_stover , slurry_temp_diff , Cellulose)
    Water = eh[0]
    Enzyme = eh[1]
    Cooling_Energy = eh[2]
    kg_Hydrolysate_per_ha = eh[3]
    
    # 600 - Fermentation 
    ethanol_to_biomass = 0.561034373 # kg of ethanol to kg of biomass
    kg_ethanol_per_ha = kg_Stover_PostDAH_per_ha * ethanol_to_biomass * 0.511 * 0.931
    kg_corn_beer_per_ha = (kg_ethanol_per_ha / 0.054 ) - kg_ethanol_per_ha
    
    # 700 - Distillation and Dehydration
    ethanol_per_kWh = 1.81 # liters of ethanol produced per kWh electricity 
    MJ_per_ethanol =7.7 # MJs of heat required per liters of ethanol produced
    kg_ethanol_to_L_ethanol = 1.267427123 # kg ethanol to liters of ethanol 
    
    dad = Process.DAD(ethanol_per_kWh , kWh_to_MJ ,kg_ethanol_per_ha ,kg_ethanol_to_L_ethanol ,
     MJ_per_ethanol , kg_Stover_PostDAH_per_ha )
    
    Electricity_per_ha = dad[0]
    Heat_per_ha = dad[1]
    kg_lignin_per_ha = dad[2]
    
    # 900 Final Product 
    fp = Process.FP ( kg_ethanol_per_ha , kg_ethanol_to_L_ethanol , gal_to_L , kg_stover_per_ha , kg_to_ton , ton_to_bu )
    L_ethanol_per_ha = fp[0]
    gal_ethanol_per_ton_stover = fp[1]
    gal_ethanol_per_bu_corn_grain = fp[2]
    
    # 1000 Scaled production
    L_ethanol_per_ha*x
    
    return 