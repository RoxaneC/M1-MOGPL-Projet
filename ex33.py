#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 20 16:26:04 2022

@author: 21205907
"""

# import exercice
from numpy import arange,array,ones,linalg
from pylab import plot,show

xi = array([4, 17, 37, 55, 88, 96])
A = array([xi, ones(6)])
y = [11, 25, 46, 48, 65, 71]
w = linalg.lstsq(A.T,y)[0]
line = w[0]*xi + w[1]
plot(xi, line, 'r-', xi, y, 'o')
show()

from gurobipy import *

nbcont=12
nbvar=8

# Range of plants and warehouses
lignes = range(nbcont)
colonnes = range(nbvar)

# Matrice des contraintes
a = [[1,0,0,0,0,0,4,1],
     [1,0,0,0,0,0,-4,-1],
     [0,1,0,0,0,0,17,1],
     [0,1,0,0,0,0,-17,-1],
     [0,0,1,0,0,0,37,1],
     [0,0,1,0,0,0,-37,-1],
     [0,0,0,1,0,0,55,1],
     [0,0,0,1,0,0,-55,-1],
     [0,0,0,0,1,0,88,1],
     [0,0,0,0,1,0,-88,-1],
     [0,0,0,0,0,1,96,1],
     [0,0,0,0,0,1,-96,-1]]


# Second membre
b = [11,-11, 25,-25, 46,-46, 48,-48, 65,-65, 71,-71]

# Coefficients de la fonction objectif
c = [1,1,1,1,1,1,0,0]

m = Model("mogplex")     
        
# declaration variables de decision
x = []
for i in range(len(colonnes)-2):
    x.append(m.addVar(vtype=GRB.CONTINUOUS, lb=0, name="x%d" % (i+1)))
    
x.append(m.addVar(vtype=GRB.CONTINUOUS, lb=-GRB.INFINITY, name="x%d" % (i+1)))
x.append(m.addVar(vtype=GRB.CONTINUOUS, lb=-GRB.INFINITY, name="x%d" % (i+1)))


# maj du modele pour integrer les nouvelles variables
m.update()

obj = LinExpr();
obj =0
for j in colonnes:
    obj += c[j] * x[j]
        
# definition de l'objectif
m.setObjective(obj,GRB.MINIMIZE)

# Definition des contraintes
for i in lignes:
    m.addConstr(quicksum(a[i][j]*x[j] for j in colonnes) >= b[i], "Contrainte%d" % i)

# Resolution
m.optimize()


print("")                
print('Solution optimale:')
for j in colonnes:
    print('x%d'%(j+1), '=', x[j].x)
print("")
print('Valeur de la fonction objectif :', m.objVal)

line = x[nbvar-2].x*xi + x[nbvar-1].x
plot(xi, line, 'r-', xi, y, 'o')
show()