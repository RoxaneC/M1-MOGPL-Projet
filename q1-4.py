#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec  1 16:16:41 2022

@author: 21205907
"""


from gurobipy import *

nbcont=5
nbvar=11

# intervalles de nos variables
lignes = range(nbcont)
colonnes_bik = [1,2,4,5]
colonnes_rk = [0,3]
colonnes_x = [6,7,8,9,10]
colonnes = [0,1,2,3,4,5,6,7,8,9,10]

# Matrice des contraintes

a = [[1, -1,  0,  0,  0,  0,  -5,  -6,  -4,  -8,  -1],
     [1,  0, -1,  0,  0,  0,  -3,  -8,  -6,  -2,  -5],
     [0,  0,  0,  1, -1,  0,  -5,  -6,  -4,  -8,  -1],
     [0,  0,  0,  1,  0, -1,  -3,  -8,  -6,  -2,  -5],
     [0,  0,  0,  0,  0,  0,   1,   1,   1,   1,   1]]


# Second membre

b = [0,0,0,0, 3]

# Coefficients de la fonction objectif

c = [1,-1,-1,2,-1,-1,0,0,0,0,0]

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
        

#for i1 in colonnes_bik:
#    x[i1] = m.addVar(vtype=GRB.CONTINUOUS, lb=0, name="x%d" % (i1+1))
#for i2 in colonnes_rk:
#    x[i2] = m.addVar(vtype=GRB.CONTINUOUS, lb=-GRB.INFINITY, name="x%d" % (i2+1))


# maj du modele pour integrer les nouvelles variables
m.update()
obj = LinExpr();
obj = 0
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
