# -*- coding: utf-8 -*-
"""
Created on Tue Jul  7 19:32:20 2020

@author: mzeigha
"""


def DAH (kg_comm_stover_ha , water_to_stover_ratio , acid_purity , NH3 , 
         H2SO4 , Cp_water , Cp_stover , Cp_H2SO4 ,temp_diff ,Total_Mass_Conv ):
    
    dilution_water = kg_comm_stover_ha * water_to_stover_ratio
    strong_acid = dilution_water * acid_purity / 100
    strong_base = ( NH3 / H2SO4 ) * strong_acid
    Heating_energy = ((dilution_water * Cp_water * temp_diff) +
    (kg_comm_stover_ha * Cp_stover *temp_diff) + (strong_acid * Cp_H2SO4 * temp_diff)) /1000
    
    kg_PreHydrolysate_Slurry_per_ha = kg_comm_stover_ha + dilution_water + strong_acid
    
    kg_Stover_PostDAH_per_ha = kg_comm_stover_ha *Total_Mass_Conv / 100
    
    return (Heating_energy)
    