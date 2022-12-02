#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec  2 14:58:57 2022

@author:    21110121
"""

from gurobipy import *

dico_sommets = {'a':1,'b':2,'c':3,'d':4,'e':5,'f':6,'g':7}

# arrêtes avec ( sommet i, sommet j, cout arrete, scénario)

E = [(1,2,5,1),(1,4,2,1),(1,3,10,1),(2,5,4,1),(2,3,4,1),(2,4,1,1),(4,3,1,1),(4,6,3,1),(3,5,3,1),(3,6,1,1),(5,7,1,1),(6,7,1,1),(1,2,3,2),(1,4,6,2),(1,3,4,2),(2,5,6,2),(2,3,2,2),(2,4,3,2),(4,3,4,2),(4,6,5,2),(3,5,1,2),(3,6,2,2),(5,7,1,2),(6,7,1,2)]
V = [1,2,3,4,5,6,7]

G = V,E


def solve(G):
    
    V,E = G
    
    m = Model("mogplex")
    
    # déclaration des variables de décision
    x = {}
    for (i,j,_,s) in E:
        x[(i,j,s)] = m.addVar(vtype=GRB.BINARY, name = "x%s%s%s"%(i,j,s))
    
    c = {}
    for (i,j,k,s) in E:
        c[(i,j,s)] = k
        
    w = [2,1]    
            
        
    m.update()
    
    # définition de l'objectif 
    
    obj = LinExpr()
    obj = 0
    for (i,j,_,s) in E:
        obj += ((-c[(i,j,s)]) * x[(i,j,s)])*w[s-1]
        
    m.setObjective(obj,GRB.MAXIMIZE)
    
    # définition des contraintes
    
    for(i,j,_,s) in E :
        if i != 1 :
            preds = [(i2,j2,s2) for (i2,j2,c2,s2) in E if(j2==i)]
            m.addConstr(x[(i,j,s)]<=quicksum([x[ind] for ind in preds]),"Contrainte conservation %s"%(i))
            
    for i in V:
        if i != 1 :
            preds = [(i2,j2,s2) for (i2,j2,c2,s2) in E if(j2==i)]
            m.addConstr(quicksum([x[ind] for ind in preds])<=1,"Contrainte unique %s"%(i))
        
    preds = [(i2,j2,s2) for (i2,j2,c2,s2) in E if j2==7]
    m.addConstr(quicksum([x[ind] for ind in preds])==1, "Contrainte atteint sommet g")
    
    m.optimize()
    
    # Affichage des résultats
    print("")                
    print('Solution optimale:')
    for (i,j,s) in x:
        print((i,j,s), '=', x[(i,j,s)].x)
              
    print("")
    print('Valeur de la fonction objectif :', m.objVal)
    
    if(m.status == GRB.INFEASIBLE):
        print("pas de chemin plus rapide")
        
# chemin le plus robuste dans les deux scénarios:
        
solve(G)
