#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec  1 16:16:41 2022

@author: 21205907
"""


from gurobipy import *


nbcont=5
nbvar=11

# Intervalles de nos variables
lignes = range(nbcont)
colonnes = range(nbvar)

# Explicitation des colonnes représentants les variables rk, bik et xi
colonnes_rk = [0,3]
colonnes_bik = [1,2,4,5]
colonnes_x = [6,7,8,9,10]

# Matrice des contraintes
a = [[1, -1,  0,  0,  0,  0,  -5,  -6,  -4,  -8,  -1],
     [1,  0, -1,  0,  0,  0,  -3,  -8,  -6,  -2,  -5],
     [0,  0,  0,  1, -1,  0,  -5,  -6,  -4,  -8,  -1],
     [0,  0,  0,  1,  0, -1,  -3,  -8,  -6,  -2,  -5],
     [0,  0,  0,  0,  0,  0,   1,   1,   1,   1,   1]]

# Second membre
b = [0,0,0,0, 3]

# Coefficients de la fonction objective
c = [1,-1,-1,2,-1,-1,0,0,0,0,0]

# Création de modèle
m = Model("mogplex")     
        
# Déclaration variables de décision
x = []
for i in colonnes:
     # les rk sont réels non bornés
    if i in colonnes_rk:
        x.append(m.addVar(vtype=GRB.CONTINUOUS, lb=-GRB.INFINITY, name="r%d" % (i+1)))
    
    # les bik sont supérieurs ou égaux à 0
    if i in colonnes_bik:
        x.append(m.addVar(vtype=GRB.CONTINUOUS, lb=0, name="b%d" % (i+1)))
          
    # les xi sont binaires (1 ou 0)
    if i in colonnes_x:
        x.append(m.addVar(vtype=GRB.BINARY, name="x%d" % (i+1)))

     
# MAJ du modèle pour integrer les nouvelles variables
m.update()
obj = LinExpr();
obj = 0
for j in colonnes:
    obj += c[j] * x[j]
        
# Définition de l'objectif (maximisation de la fonction objectif)
m.setObjective(obj,GRB.MAXIMIZE)

# Définition des contraintes
for i in lignes:
    m.addConstr(quicksum(a[i][j]*x[j] for j in colonnes) <= b[i], "Contrainte%d" % i)
    
# Résolution
m.optimize()

# Affichage des résultats
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
