#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec  1 14:14:46 2022

@author: 21205907
"""
import numpy as np
from gurobipy import *

# nb d'agents
n = 3
# nb d'objets
p = 6
# utilité
z = [325, 225, 210, 115, 75, 50]
# pondération
w = [3,2,1]
w_2 = [1,1,1]

nbcont = n*p
print(nbcont)
nbvar = (p+1)*n
print(nbvar)

# intervalles de nos variables
lignes = range(10)
colonnes = range(18)

colonnes_rk = [0,4,8]
colonnes_bik = [1,2,3,5,6,7,9,10,11]
colonnes_x = [12,13,14,15,16,17]

# Matrice des contraintes


a = [[1, -1,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  -325, -225, -210, -115, -75, -50],
     [1,  0, -1,  0,  0,  0,  0,  0,  0,  0,  0,  0,  -325, -225, -210, -115, -75, -50],
     [1,  0,  0, -1,  0,  0,  0,  0,  0,  0,  0,  0,  -325, -225, -210, -115, -75, -50],
     [0,  0,  0,  0,  1, -1,  0,  0,  0,  0,  0,  0,  -325, -225, -210, -115, -75, -50],
     [0,  0,  0,  0,  1,  0, -1,  0,  0,  0,  0,  0,  -325, -225, -210, -115, -75, -50],
     [0,  0,  0,  0,  1,  0,  0, -1,  0,  0,  0,  0,  -325, -225, -210, -115, -75, -50],
     [0,  0,  0,  0,  0,  0,  0,  0,  1, -1,  0,  0,  -325, -225, -210, -115, -75, -50],
     [0,  0,  0,  0,  0,  0,  0,  0,  1,  0, -1,  0,  -325, -225, -210, -115, -75, -50],
     [0,  0,  0,  0,  0,  0,  0,  0,  1,  0,  0, -1,  -325, -225, -210, -115, -75, -50],
     [0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  1, 1, 1, 1, 1, 1]]

   

# Second membre
## même utilité pour tout le monde (valeur objective d'un objet)
b = [0,0,0,0,0,0,0,0,0,6]

# Coefficients de la fonction objectif
c = [1,-1,-1,-1,2,-1,-1,-1,3,-1,-1,-1,0,0,0,0,0,0]

#c = np.kron(w_2, c_aux)
#c[colonnes_rk] += [0,1,2]

m = Model("mogplex")     
        
# declaration variables de decision
x = []
for i in colonnes:
    if i in colonnes_rk:
        x.append(m.addVar(vtype=GRB.CONTINUOUS, lb=-GRB.INFINITY, name="r%d" % (i+1)))
    if i in colonnes_bik:
        x.append(m.addVar(vtype=GRB.CONTINUOUS, lb=0, name="b%d" % (i+1)))
    if i in colonnes_x:
        x.append(m.addVar(vtype=GRB.BINARY, name="x%d" % (i+1)))

# maj du modele pour integrer les nouvelles variables

m.update()
obj = LinExpr();
obj =0
for j in colonnes:
    obj += c[j] * x[j]
        
# definition de l'objectif

m.setObjective(obj,GRB.MAXIMIZE)

# Definition des contraintes

for i in lignes:
    m.addConstr(quicksum(a[i][j]*x[j] for j in colonnes) <= b[i], "Contrainte%d" % i)

# Resolution

m.optimize()


print("")                
print('Solution optimale:')
for j in colonnes:
    if j in colonnes_rk:
        print('r%d'%(j+1), '=', x[j].x)
    if j in colonnes_bik:
        print('b%d'%(j+1), '=', x[j].x)
    if j in colonnes_x:
        print('x%d'%(j+1), '=', x[j].x)
print("")
print('Valeur de la fonction objectif :', m.objVal)