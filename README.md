### **Poitevin Eve**
# Projet Accés et Recherche d'Informations


Pendant 6 séances, nous avons travaillé sur 3 TP différents qui nous ont permis de découvrir la loi de Zipf, la constitution de vocabulaire et la recherche de requête dans des documents.
Nous allons ici, pour chaque TP faire le point sur les choix que nous avons fait.

## TP1 Loi de Zipf

Le but de ce TP était de manipuler une collection de documents afin d'illustrer la loi de Zipf.

Premièrement, nous avons utilisé la fonction **ExtractionDesFichiers** fournie afin de découper **cacm.all** en une liste de fichiers dans un répertoire.
Nous avons ensuite implémenté la fonction **TokenizeFile** dans le fichier **tokenize_cacm.py**.

Cette fonction a pour but d'ouvrir tous les fichiers, issus du découpage de cacm.all fait précédemment,
pour ne garder de chaque fichier que les mots qui commencent par une lettre et qui ne contiennent ensuite que des lettres ou des chiffres.

Pour effectuer le découpage des mots, on utilise donc un tokenizer, qui va utiliser une expression régulière afin de savoir comment découper la chaine de caractères.
Une fois que le tokenizer a séparé une chaine de caractère en liste de mots, il ne nous reste plus qu'à les écrire ensuite (en minuscules) dans le nouveau fichier.

L'objectif caché de cette étape et de faciliter le traitement de nos données par la suite. C'est pourquoi nous avons choisi d'écrire un unique mot par ligne dans les fichiers nouvellement créés par cette fonction. Ce choix nous permet alors, par la suite, d'avoir accès aux mots indépendamment les uns des autres, en faisant une simple lecture ligne par ligne.

Comme dit précédemment, l'objectif est donc dorénavant d'utiliser la collection de documents créée, afin de l'analyser.

Pour commencer, on souhaite connaitre la fréquence d'apparition de tous les termes de la collection.
Ainsi, pour ce faire on créer un dictionnaire python dans lequel on stocke la fréquence d'apparition de chaque mot.

Pour la suite, afin de faciliter l'analyse de ces données, on choisit de les afficher par ordre décroissant d'occurrences.

Pour finir avec cette première partie sur la loi de Zipf, on souhaite donc faire apparaitre la taille du vocabulaire, ainsi que la valeur du lambda théorique calculé, qui se calcule avec la formule mathématique suivante : **lambda_th = nb_occ/np.log(dico_size)**

## TP2 Constitution de vocabulaire et représentation

L'objectif pour ce TP, a été de créer le vocabulaire associé à la collection, que nous avons précédemment constitué, et représenter notre modèle suivant le modèle de Salton, utilisant des vecteurs et l'index inversé.

Pour commencer, il nous faut alors dans un premier temps définir notre anti-dictionnaire, en parcourant le fichier **common_words** et en ajoutant chaque mot à l'anti-dictionnaire, si celui-ci n'y est pas déjà.
On souhaite ensuite filtrer notre collection avec cet anti-dictionnaire, et stocker le résultat. Pour cela, on ouvre chaque fichier un par un et on leur applique l'anti-dictionnaire, c'est-à-dire que pour chaque mot de ce fichier, on l'écrit dans le nouveau fichier que s'il ne se trouve pas dans l'anti-dictionnaire.
De plus, on utilise la troncature de Porter (grâce aux stemmer de la bibliothèque nltk) pour tronquer et stocker les mots.

On va ensuite créer le vocabulaire, en construisant un dictionnaire, qui a comme clé les mots présents dans la collection et comme valeur 0. Pour ce faire, on a fait le choix d'intégrer la création de ce vocabulaire au code qui s'occupe d'appliquer l'anti-dictionnaire, afin d'éviter une revue supplémentaire des fichiers. 

Ensuite, on souhaite calculer le nombre d'apparition d'un mot dans un document, mais également le nombre de documents dans lequel ce mot apparait. Ainsi, pour les mêmes raisons que précédemment, nous choisissons d'effectuer ce calcul en même temps que l'application de l'anti-dictionnaire à notre collection.

Une fois cela fait, nous souhaitons construire la représentation vectorielle de tous les documents d'après le modèle vectoriel de Salton. Nous réalisons ceci dans la fonction **RepresentationVectorielle**, qui utilise elle même une fonction **tf** qui calcule le nombre d'occurrences de chaque mot dans un document.

Nous souhaitons dorénavant, à partir du vocabulaire et des vecteurs des documents, construire l'index inversé de ses termes. Pour cela, on parcourt le vocabulaire et pour chaque mot, on parcourt les vecteurs, ainsi on ajoute le document en clé et le **tf * idf** en valeur. 

Pour finir, nous allons calculer la norme de chaque document. Pour cela, on parcourt notre dictionnaire de vecteurs, puis on calcule `norme = sqrt(somme((tf * idf)²))` pour chaque fichier.

## TP3 Recherche et évaluation

Le but de cette partie était de développer un modèle vectoriel sur la base de la représentation VSM.
L'objectif de cette dernière partie est d'être capable de récupérer une requête et de renvoyer une liste de documents répondant au mieux à celle-ci.

Pour cela, on commence par récupérer l'index inversé, le dictionnaire ainsi que les normes des documents et on construit notre anti-dictionnaire.
Dans un premier temps, il nous faut récupérer la requête utilisateur puis effectuer une boucle, tant que cette requête n'est pas traitée, c'est-à-dire, qu'elle n'est pas vide.

Ensuite, pour chaque requête, on la tokenize et passe chaque token qui en résulte, dans l'anti-dictionnaire. Puis, on détermine le vecteur correspondant à la requête et calcule tf et tf*idf, et on stocke la norme de la requête q : norme_q = sqrt(somme(carré).
Alors, si la norme de la requête est égale à 0, on arrête la recherche car cela signifie qu'aucun document ne correspond à cette requête.

Par contre, si la norme de la requête est non nulle, alors on calcule, grace à l'index inversé, le produit scalaire entre requête et document, puis on divise ces résultats par la norme de document * norme de requete, et on trie les réponses par ordre de pertinence décroissante.

Pour finir, on affiche, en fonction de la demande que fait l'utilisateur, les documents les plus pertinents correspondant à la requête.