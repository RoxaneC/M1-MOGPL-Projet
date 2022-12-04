# M1-MOGPL-Projet

Ce projet à pour but de réflechir sur des questions d'optimisation équitable. Le code présent ici répond à plusieurs cas particuliers mentionnés dans l'article joint au sujet.

## Prérequis

Ce projet a été développé en Python3 et requiert donc un executeur python.

Il utilise divers modules qui sont indispensables à son fonctionnement :

* gurobipy              (résolution de programme linéaire)
* numpy                 (simplification de l'usage des listes)
* scipy.linalg          (simplification de construction de matrice par blocs)
* time                  (calcul du temps d'execution)
* matplotlib.pyplot     (affichage et sauvegarde des graph)

Ces modules peuvent être installé si besoin par la commande `pip install <nom_du_module>`

## Descriptions

L'archive est découpée en 4 sous dossiers correspondant chacun au code de la partie du sujet correspondante. Il faut en extraire les dossiers pour pouvoir executer les différentes parties.

Le dossier `partie1` contient le code répondant à la question 4 de la première partie (exemple 1 du sujet).

Le dossier `partie2` contient le code répondant aux problematiques de la deuxième partie :

* Le fichier `part2Explicite.py` décrit de manière explicite les définitions des différentes matrices pour le premier exemple de l'article. Les valeurs de la matrice des contraintes, du second membre et de la fonction objectif sont entrée à la main en suivant le raisonnement indiqué dans le rapport.
* Le fichier `part2Automatique.py` automatise pour des entrées différentes la résolution du problème d'affectation d'objets selon le nombre de personnes et leurs utilités relatives.
* Le fichier `part2Verif.py` vérifie le bon fonctionnement de la formule automatique de résolution suivant l'exemple de l'article.
* Le fichier `part2Tests.py` effectue plusieurs tests de résolution selon des nomdres d'agents, d'objets, et des valeurs d'utilités différentes. Il effectue également un calcul moyen du temps d'execution selon ces paramètres. (attention, suivant l'aléatoire, le temps d'execution peut devenir très long; `Ctrl + C` permet de sortir de la boucle actuelle et donc de forcer la fin de calcul pour l'instance en cours).

Le dossier `partie3` contient le code répondant aux problematiques de la troisième partie :

* Le fichier `part3Explicite.py` décrit de manière explicite les définitions des différentes matrices pour le deuxième exemple de l'article. Les valeurs de la matrice des contraintes, du second membre et de la fonction objectif sont entrée à la main en suivant le raisonnement indiqué dans le rapport.
* Le fichier `part3Automatique.py` automatise pour des entrées différentes la résolution du problème d'acceptation de projets selon les objectifs et leurs utilités relatives.
* Le fichier `part3Verif.py` vérifie le bon fonctionnement de la formule automatique de résolution suivant l'exemple de l'article.
* Le fichier `part3Tests.py` effectue plusieurs tests de résolution selon des nomdres d'agents, d'objets, et des valeurs d'utilités différentes. Il effectue également un calcul moyen du temps d'execution selon ces paramètres.

## Éxecution

Pour executer l'un des programmes, utiliser dans un terminal dans le repertoire courant :
`python </partieX/nom_du_fichier.py>`   (remplacer X par la partie concernée)

## Auteurs

Développé par CELLIER Roxane et REY Soraya