#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec  2 18:11:12 2022

@author: 21205907
"""

from gurobipy import *
import numpy as np
from scipy.linalg import block_diag
import time
import matplotlib.pyplot as plt


def resolution(n,p,U,C,B,w):
    
    # calcul de w'
    w_prime = [w[i] - w[i+1] for i in range(len(w)-1)]
    w_prime.append(w[-1])
    
    
    ## AUTOMATISATION SELON LES PARAMÈTRES
    # sous matrice représentant les contraintes sur rk et bik
    sm_rkbik = np.bmat([np.ones((n,1)), -1*np.eye(n)])
    sm_rb = np.kron(np.eye(n), sm_rkbik)

    # sous mtrice représentant les contraintes sur les zi(x) (utilités)
    sm_zi = np.multiply(U, -1)
    sm_z = np.kron(np.ones((n,1)), sm_zi)

    # sous matrice représentant la contrainte des coûts de projet
    sm_x = [C]

    # sous matrice pour le remplissage par 0
    sm_zero = np.zeros((1, (n+1)*n))

    # assemblage de la matrice des contraintes
    a = np.bmat( [[sm_rb, sm_z], [sm_zero, sm_x]] ).tolist()
    print(a)

          
    # Récupération des nombre de variables, contraintes, etc
    nbVar = n*(n+1) + p
    nbCont = len(a)
    lignes = range(nbCont)
    colonnes = range(nbVar)
    
    # Facilite la lecture du résultat
    list_names = []
    for i in range(p):
        s = "x_" + str(i+1)
        list_names.append(s)
            
            
    # Explicitation des indices des colonnes représentants les variables rk, bik et xi
    colonnes_rk = [i*(n+1) for i in range(n)]
    colonnes_bik = [i for i in range(n*(n+1)) if i not in colonnes_rk]
    colonnes_x = [i for i in range(n*(n+1), nbVar)]
    
    
    # Second membre
    b = np.concatenate((np.zeros(n*n), B), axis=None)
    print(list_names)

    # Coefficients de la fonction objectif
    c = []
    for i in range(n):
        aux = np.concatenate( (i+1, -1*np.ones((1,n))), axis = None) * w_prime[i]
        c.extend(aux.tolist())

    for i in range(len(colonnes_x)):
        c.append(0)
        


    ## RÉSOLUTION
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
            
    # MAJ du modèle pour integrer les nouvelles variables
    m.setObjective(obj,GRB.MAXIMIZE)

    # Définition des contraintes
    for i in lignes:
        m.addConstr(quicksum(a[i][j]*x[j] for j in colonnes) <= b[i], "Contrainte%d" % i)

    # Résolution
    m.optimize()


    # Affichage des résultats
    print("")                
    print('Solution optimale:')
    ind=0
    for j in colonnes_x:
        print(list_names[ind], '=', x[j].x)
        ind+=1
              
    print("")
    print('Valeur de la fonction objectif :', m.objVal)
    
    pass


## VÉRIFICATION ET TESTS AVEC L'EXEMPLE DE L'ARTICLE
# nb d'agents
n = 2
# nb d'objets
p = 4
# utilité
U = [[19,6,17,2],
     [2,11,4,18]]
# cout
C = [40,50,60,50]
# budget
B = 100
# pondération
w1 = [2,1]
w2 = [10,1]
w3 = [1/2,1/2]

resolution(n,p,U,C,B,w1)
resolution(n,p,U,C,B,w2)
resolution(n,p,U,C,B,w3)


## TESTS ET CALCUL DU TEMPS D'ÉXECUTION
N = [5,10,15]
tps = []
for n in N:
    plt.figure()
    p = 5*n
    tps_N = []
    
    for i in range(4):
        U = np.random.randint(100, size=(n,p)).tolist()
        w = np.random.randint(2*n, size=n).tolist()
        w.sort(reverse=True)
        
        debut = time.time()
        resolution(n,p,U,w)
        fin = time.time()
        tps_N.append(fin - debut)
        
    tps.append(np.mean(tps_N))
        
plt.title("Temps d'execution selon N")
plt.xlabel("n (nombre d'agents)")
plt.ylabel("tps (temps d'éxecution')")
plt.plot(N, tps)
plt.show()
