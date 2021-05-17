
"""
Created on Fri Jul  3 16:20:20 2020

@author: jkern
"""

import numpy as np
import pandas as pd

def sim(kg_stover):
    
    ###################################
    # CONVERSIONS
    S = np.array(kg_stover)
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
    # BIOPROCESS NAD CONVERSION 200 - 600
     
    # 200 - Size Reduction Process - Comminution 
    Comminution_Electricity = S * Percent_to_hammer_mill / 100 #MJ
    kg_comm_stover = S * Comminution_energy # kg comminuted stover 
    
    # 300 - Dilute acid hydrolysis 
    
    # Yeild & Conversions:
    Matrl_Handling_Energy = 241.79 # MJ
    water_to_stover_ratio = 4
    acid_purity = 8 # acide weight percent (%)
    H2SO4 = 98.079 # H2SO4 molar mass
    NH3 = 17.031 # NH3 molar mass
    Cp_water = 4.184 # water heat capacity kJ/kg C
    Cp_stover = 1.03 # Stover heat capacity kJ/kg C 
    Cp_H2SO4 = 1.34 # H2SO4 heat capacity kJ/kg C
    final_temp = 175 # degree C
    int_temp = 20 # degree C 
    temp_diff = final_temp - int_temp # Temprture difference that the mixture should be heated (degree C)
    
    # Conversion rates:
    Cellulose = 0.4105
    Cellulose_to_Glucose = 81.3 # %
    Hemicellulose_to_Xylose = 67 # %
    Total_Mass_Conv = 97.3 # %
    
    dilution_water = kg_comm_stover * water_to_stover_ratio
    strong_acid = dilution_water * acid_purity / 100
    strong_base = ( NH3 / H2SO4 ) * strong_acid
    heating_energy = ((dilution_water * Cp_water * temp_diff) + (kg_comm_stover * Cp_stover *temp_diff) + (strong_acid * Cp_H2SO4 * temp_diff)) /1000
    kg_PreHydrolysate_Slurry = kg_comm_stover + dilution_water + strong_acid
    kg_Stover_PostDAH = kg_comm_stover *Total_Mass_Conv / 100
        
    # 400 - Enzymatic Hydrolysis
    #Conversions and Yield
    Water_to_Prehydrolysate = 4 # Ratio
    Cellulase_to_Cellulose = 0.02 # Ratio
    slurry_int_temp = 175 # dgree C
    slurry_final_temp = 48 # degree C
    slurry_temp_diff = slurry_int_temp - slurry_final_temp
    
    Water = kg_Stover_PostDAH * water_to_stover_ratio
    Enzyme = kg_Stover_PostDAH * Cellulase_to_Cellulose * Cellulose
    Cooling_Energy = kg_Stover_PostDAH * Cp_stover * slurry_temp_diff /1000
    kg_Hydrolysate = kg_Stover_PostDAH + Water + Enzyme

    
    # 600 - Fermentation 
    ethanol_to_biomass = 0.561034373 # kg of ethanol to kg of biomass
    kg_ethanol = kg_Stover_PostDAH * ethanol_to_biomass * 0.511 * 0.931
    kg_corn_beer = (kg_ethanol / 0.054 ) - kg_ethanol
    
    # 700 - Distillation and Dehydration
    ethanol_per_kWh = 1.81 # liters of ethanol produced per kWh electricity 
    MJ_per_ethanol =7.7 # MJs of heat required per liters of ethanol produced
    kg_ethanol_to_L_ethanol = 1.267427123 # kg ethanol to liters of ethanol 
    
    Electricity = (1 / ethanol_per_kWh) * kWh_to_MJ * kg_ethanol * kg_ethanol_to_L_ethanol
    Heat = MJ_per_ethanol * kg_ethanol * kg_ethanol_to_L_ethanol
    kg_lignin = 0.18 * kg_Stover_PostDAH
    
    # 900 Final Product 
    L_ethanol = kg_ethanol * kg_ethanol_to_L_ethanol
    # gal_ethanol_per_ton_stover = ( L_ethanol / gal_to_L ) / (S * kg_to_ton )
    # gal_ethanol_per_bu_corn_grain = gal_ethanol_per_ton_stover / ton_to_bu 
   
    
    # 1000 Scaled production
    
    return L_ethanol