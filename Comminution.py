# -*- coding: utf-8 -*-
"""
Created on Tue Jul  7 16:04:57 2020

@author: mzeigha
"""


def COMM (kg_stover_per_ha , Comminution_energy , Percent_to_hammer_mill):
    
    Comminution_Electricity = kg_stover_per_ha * Percent_to_hammer_mill / 100
    kg_comm_stover_ha = kg_stover_per_ha * Comminution_energy
    
    return (Comminution_Electricity , kg_comm_stover_ha)