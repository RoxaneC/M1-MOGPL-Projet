import numpy as np
import time
import matplotlib.pyplot as plt

from part3Automatique import resolutionCoutBudget


## TESTS ET CALCUL DU TEMPS D'ÉXECUTION
N = [2,5,10]
P = [5,10,15,20]

# stockage des temps moyens pour chaque N
tps_moy = []

# boucle de test sur différents n
for n in N:
    # stocke les temps des 10 instances pour ce n
    tps_N = []

    # valeurs de pondération arbitrairement choisies entre 0 et 2*n
    w = np.random.randint(2*n, size=n).tolist()
    # tri dans l'ordre décroissant du vecteur des pondérations
    w.sort(reverse=True)

    # boucle de test sur différents p
    for p in P:
        
        # boucle de test sur 10 instances
        for i in range(10):
            # valeurs d'utilité arbitrairement choisies entre 0 et 100
            U = np.random.randint(100, size=(n,p)).tolist()
            #C=
            #B=
            
            # execution et calcul du temps
            debut = time.time()
            #resolutionCoutBudget(n,p,U,C,B,w)
            fin = time.time()
            tps_N.append(fin - debut)
            
        # calcul et stockage du temps moyen pour n
        tps_moy.append(np.mean(tps_N))
        

# Affichage des temps d'execution pour meilleure interprétation
plt.figure()
plt.title("Temps d'execution selon N")
plt.xlabel("n (nombre d'agents)")
plt.ylabel("tps (temps d'éxecution')")
plt.plot(N, tps_moy)
plt.show()
