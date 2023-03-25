# -*- coding: utf-8 -*-
"""
Created on Tue Jun 20 22:14:07 2017

@author: YSu
"""

from pyomo.opt import SolverFactory
from biofuel_LP import model as m1
from pyomo.core import Var
from pyomo.core import Constraint
from pyomo.core import Param
from operator import itemgetter
import pandas as pd
import numpy as np
from datetime import datetime
import pyomo.environ as pyo
from pyomo.environ import value

instance = m1.create_instance('biofuels_data.dat')
instance.dual = pyo.Suffix(direction=pyo.Suffix.IMPORT)

Solvername = 'cplex'

opt = SolverFactory(Solvername)
    
# opt.options['threads'] = Threadlimit

result = opt.solve(instance,tee=True,symbolic_solver_labels=True, load_solutions=False) ##,tee=True to check number of variables\n",
instance.solutions.load_from(result)  

land_usage = []
    
for v in instance.component_objects(Var, active=True):
    varobject = getattr(instance, str(v))
    a=str(v)
              
    if a=='land_usage':
        for index in varobject:
            land_usage.append((index[0],index[1],varobject[index].value))
                    
     
land_usage=pd.DataFrame(land_usage,columns=('Feedstock','District','Value'))
land_usage.to_csv('land_usage_out_district_level_GHG_20.csv',index=None)


