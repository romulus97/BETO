"""
Created on Tue Jul  7 15:29:48 2020

@author: mzeigha
"""


def TRK (kg_stover_per_ha, Truck_Capasity):
    
    num_of_Trucks = kg_stover_per_ha / (Truck_Capasity * 1000)

    return (num_of_Trucks)