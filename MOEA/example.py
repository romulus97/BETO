# -*- coding: utf-8 -*-
"""
Created on Sun Sep  6 03:32:06 2020

@author: jkern
"""

from platypus import NSGAII, Problem, Real

def belegundu(vars):
    x = vars[0]
    y = vars[1]
    return [-2*x + y, 2*x + y], [-x + y - 1, x + y - 7]

problem = Problem(2, 2, 2)
problem.types[:] = [Real(0, 5), Real(0, 3)]
problem.constraints[:] = "<=0"
problem.function = belegundu

algorithm = NSGAII(problem)
algorithm.run(100)