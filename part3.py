#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec  1 17:23:19 2022

@author: 21205907
"""

import numpy as np
from gurobipy import *

# nb d'agents
n = 2
# nb d'objets
p = 4
# pondération
w = [2,1]
w_2 = [1,1]

#cout et budget
cout = [40,50,60,50]
budget = 100

nbcont = n*p
print(nbcont)
nbvar = (p+1)*n
print(nbvar)

# intervalles de nos variables
lignes = range(nbcont)
colonnes = range(nbvar)

colonnes_rk = [(p+1)*i for i in range(n)]
colonnes_bik = [i for i in range(nbvar) if i not in colonnes_rk ]

# Matrice des contraintes


a = [[1, -1,  0,  0,  0,  0,  0,  0,  0,  0],
     [1,  0, -1,  0,  0,  0,  0,  0,  0,  0],
     [1,  0,  0, -1,  0,  0,  0,  0,  0,  0],
     [1,  0,  0,  0, -1,  0,  0,  0,  0,  0],
     [0,  0,  0,  0,  0,  1, -1,  0,  0,  0],
     [0,  0,  0,  0,  0,  1,  0, -1,  0,  0],
     [0,  0,  0,  0,  0,  1,  0,  0, -1,  0],
     [0,  0,  0,  0,  0,  1,  0,  0,  0, -1]]
   

# Second membre
## même utilité pour tout le monde (valeur objective d'un objet)
b = [19,6,17,2,2,11,4,18]

# Coefficients de la fonction objectif
c = [1,-1,-1,-1,-1,2,-1,-1,-1,-1]

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
print("")
print('Valeur de la fonction objectif :', m.objVal)