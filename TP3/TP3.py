from collections import defaultdict
import os
from nltk.stem.porter import *
import json
import math
import numpy
from nltk.tokenize import RegexpTokenizer

docs_path = "/home/eve/Documents/Polytech_Grenoble/4A/S8/MRI/TP1/collection/"
antidic_path = "/home/eve/Documents/Polytech_Grenoble/4A/S8/MRI/TP1/cacm/common_words"
tp2_path = "/home/eve/Documents/Polytech_Grenoble/4A/S8/MRI/TP2/"

tokenizer = RegexpTokenizer('[A-Za-z]{1,}')

# Définition de l'antidictionnaire
anti_dico = defaultdict(lambda: 0)

def DefAntiDico(infile):
    fileHandler = open (infile, "r")
    lines = fileHandler.readlines()
    for line in lines :
        line = line.lower()
        line = str.rstrip(line)
        if (line in anti_dico):
            continue
        else:
            anti_dico[line] = 1
    fileHandler.close()
    return(anti_dico)

DefAntiDico(antidic_path)

# nom d'un fichier CACM-xxx.flt passé en paramètre et affiche le fichier CACM-xxx appartenant à collection
def AfficherCACM(filename):
    filename = filename.split(".")
    print(filename[0] + " : \n\n")
    file = open(filename[0], "r")
    file_contents = file.read()
    print(file_contents)
    file.close()

# 1. Charger l'index inversé

fileJson = open(tp2_path+"index_inverse.json", "r")
index_inverse = json.load(fileJson)
fileJson.close()

# 2. Charger le dictionnaire

fileJson = open(tp2_path+"vocabulaire.json", "r")
vocabulaire = json.load(fileJson)
fileJson.close()

# 3. Charger les normes des documents

fileJson = open(tp2_path+"norme.json", "r")
norme = json.load(fileJson)
fileJson.close()

# 4. Boucle tant que requête non vide

# # I. Acquérir une requête q (tapée à la main)

q = input("Veuillez saisir votre requête : ")

# Boucle tant que q non vide
while q: 

    # # II. Transformer q en un vecteur vq

    # Découper q en mots
    
    q_words = tokenizer.tokenize(q)

    # TRAITEMENT DES MOTS (retrait de l'anti dico et passage à la racine via Stemmer)
    
    q_words_clean = q_words
    stemmer = PorterStemmer()

    for word in q_words:
        if word in anti_dico:
            while word in q_words_clean:
                q_words_clean.remove(word)

    for i in range(len(q_words_clean)):
        q_words_clean[i] = stemmer.stem(q_words_clean[i])

    vq = {}

    # PONDÉRATION

    # Calcul tf
    for word in q_words_clean:
        if (word in vq):
            vq[word] = vq[word] + 1
        else :
            vq[word] = 1

    # Calcul tf*idf
    for word in vq:
        if(word not in vocabulaire):
            vq[word] = 0
        else:
            vq[word] = vq[word] * vocabulaire[word]

    # NORME

    sum_q = 0

    for word in vq:
        sum_q = sum_q + pow(vq[word], 2)
    
    nvq = numpy.sqrt(sum_q)

    # print("La norme de la requête '" + q + "' est : " + str(norme_q) + "\n")

    if(nvq != 0):

        # # III. 

        # # # a) Calcul du produit scalaire entre requête et document

        resultat_partiel = {}

        for word in vq:
            if word in index_inverse:
                for cacm in index_inverse[word]:
                    if cacm in resultat_partiel:
                        resultat_partiel[cacm] = resultat_partiel[cacm] + vq[word] * index_inverse[word][cacm]
                    else:
                        resultat_partiel[cacm] = vq[word] * index_inverse[word][cacm]

        # # # b) Division des scores par "la norme de d * la norme de q"

        for cacm in resultat_partiel:
            resultat_partiel[cacm] = resultat_partiel[cacm] / (norme[cacm]*nvq)

        # # IV. Trier les réponses par ordre de pertinence décroissante

        resultat_partiel = sorted(resultat_partiel.items(), key=lambda x: x[1], reverse=True)

        # # V. Afficher les n (constante) premiers documents les plus pertinents la réponse

        n = input("Combien de premiers documents pertinents souhaitez-vous afficher ? ")

        n_docs = 0

        for i in range(int(n)):
            AfficherCACM(docs_path+resultat_partiel[i][0])

        # for filename in os.listdir(docs_path):
        #     while (n_docs < n) :
        #         file = open(docs_path+filename, "r")
        #         print(file)
        #         file.close()
        #         n_docs += 1
            


    else:
        print("Aucun document ne permet de traiter la requête")

    q = input("\nVeuillez saisir votre requête \n\nSi vous souhaitez arrêter le programme, veuillez écrire 'stop' : ")

    if (q=='stop'):
        break