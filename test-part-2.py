import numpy as np
import time
import matplotlib.pyplot as plt

from part2Automatique import resolutionUtilite


## TESTS ET CALCUL DU TEMPS D'ÉXECUTION
N = [5,10,15,20]

# stockage des temps moyens pour chaque N
tps_moy = []

# boucle de test sur différents n
for n in N:
    p = 5*n

    # stocke les temps des 10 instances pour ce n
    tps_N = []
    
    # boucle de test sur 10 instances
    for i in range(10):
        # valeurs d'utilité arbitrairement choisies entre 0 et 100
        U = np.random.randint(100, size=(n,p)).tolist()
        # valeurs de pondération arbitrairement choisies entre 0 et 2*n
        w = np.random.randint(2*n, size=n).tolist()
        # tri dans l'ordre décroissant du vecteur des pondérations
        w.sort(reverse=True)
        
        # execution et calcul du temps
        debut = time.time()
        resolutionUtilite(n,p,U,w)
        fin = time.time()
        tps_N.append(fin - debut)
        
    # calcul et stockage du temps moyen pour n
    tps_moy.append(np.mean(tps_N))
        

# Affichage et sauvegarde des temps d'execution pour une meilleure interprétation
plt.figure()
plt.title("Temps d'execution selon N")
plt.xlabel("n (nombre d'agents)")
plt.ylabel("tps (temps d'éxecution')")
plt.plot(N, tps_moy, 'r')
plt.savefig('/graph/tps_execution_part2.png')
plt.show()
