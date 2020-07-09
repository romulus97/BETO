# -*- coding: utf-8 -*-
"""
Created on Thu Jul  9 02:21:40 2020

@author: mzeigha
"""


def EH ( kg_Stover_PostDAH_per_ha , water_to_stover_ratio , Cellulase_to_Cellulose , Cp_stover , slurry_temp_diff , Cellulose):
    
    Water = kg_Stover_PostDAH_per_ha * water_to_stover_ratio
    Enzyme = kg_Stover_PostDAH_per_ha * Cellulase_to_Cellulose * Cellulose
    Cooling_Energy = kg_Stover_PostDAH_per_ha * Cp_stover * slurry_temp_diff /1000
    kg_Hydrolysate_per_ha = kg_Stover_PostDAH_per_ha + Water + Enzyme
    
    return ( Water , Enzyme , Cooling_Energy , kg_Hydrolysate_per_ha )