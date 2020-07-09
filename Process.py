# -*- coding: utf-8 -*-
"""
Created on Thu Jul  9 12:16:14 2020

@author: mzeigha
"""


def COMM (kg_stover_per_ha , Comminution_energy , Percent_to_hammer_mill):
    
    Comminution_Electricity = kg_stover_per_ha * Percent_to_hammer_mill / 100
    kg_comm_stover_ha = kg_stover_per_ha * Comminution_energy
    
    return (Comminution_Electricity , kg_comm_stover_ha)

######################################
    
def DAH (kg_comm_stover_ha , water_to_stover_ratio , acid_purity , NH3 , 
         H2SO4 , Cp_water , Cp_stover , Cp_H2SO4 ,temp_diff ,Total_Mass_Conv ):
    
    dilution_water = kg_comm_stover_ha * water_to_stover_ratio
    strong_acid = dilution_water * acid_purity / 100
    strong_base = ( NH3 / H2SO4 ) * strong_acid
    Heating_energy = ((dilution_water * Cp_water * temp_diff) +
    (kg_comm_stover_ha * Cp_stover *temp_diff) + (strong_acid * Cp_H2SO4 * temp_diff)) /1000
    
    kg_PreHydrolysate_Slurry_per_ha = kg_comm_stover_ha + dilution_water + strong_acid
    
    kg_Stover_PostDAH_per_ha = kg_comm_stover_ha *Total_Mass_Conv / 100
    
    
    
    return (Heating_energy , kg_PreHydrolysate_Slurry_per_ha , kg_Stover_PostDAH_per_ha )

######################################
    
def EH ( kg_Stover_PostDAH_per_ha , water_to_stover_ratio , Cellulase_to_Cellulose , Cp_stover , slurry_temp_diff , Cellulose):
    
    Water = kg_Stover_PostDAH_per_ha * water_to_stover_ratio
    Enzyme = kg_Stover_PostDAH_per_ha * Cellulase_to_Cellulose * Cellulose
    Cooling_Energy = kg_Stover_PostDAH_per_ha * Cp_stover * slurry_temp_diff /1000
    kg_Hydrolysate_per_ha = kg_Stover_PostDAH_per_ha + Water + Enzyme
    
    return ( Water , Enzyme , Cooling_Energy , kg_Hydrolysate_per_ha )

######################################
    
def DAD (ethanol_per_kWh , kWh_to_MJ ,kg_ethanol_per_ha ,kg_ethanol_to_L_ethanol 
         , MJ_per_ethanol , kg_Stover_PostDAH_per_ha):
    
    Electricity_per_ha = (1 / ethanol_per_kWh) * kWh_to_MJ * kg_ethanol_per_ha * kg_ethanol_to_L_ethanol
    Heat_per_ha = MJ_per_ethanol * kg_ethanol_per_ha * kg_ethanol_to_L_ethanol
    kg_lignin_per_ha = 0.18 * kg_Stover_PostDAH_per_ha
    
    return ( Electricity_per_ha , Heat_per_ha , kg_lignin_per_ha )

######################################
    
def FP ( kg_ethanol_per_ha , kg_ethanol_to_L_ethanol , gal_to_L , kg_stover_per_ha , kg_to_ton , ton_to_bu ):
    
    L_ethanol_per_ha = kg_ethanol_per_ha * kg_ethanol_to_L_ethanol
    gal_ethanol_per_ton_stover = ( L_ethanol_per_ha / gal_to_L ) / (kg_stover_per_ha * kg_to_ton )
    gal_ethanol_per_bu_corn_grain = gal_ethanol_per_ton_stover / ton_to_bu 
    
    return (L_ethanol_per_ha , gal_ethanol_per_ton_stover , gal_ethanol_per_bu_corn_grain)

######################################