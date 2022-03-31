from collections import defaultdict
import os
from nltk.stem.porter import *
import json
import math
import numpy
from ../TP2/TP2 import DefAntiDico

inpath = "/home/eve/Documents/Polytech_Grenoble/4A/S8/MRI/TP1/collection_tokens/"
antidicpath = "/home/eve/Documents/Polytech_Grenoble/4A/S8/MRI/TP1/cacm/common_words"
outpath = "/home/eve/Documents/Polytech_Grenoble/4A/S8/MRI/TP2/"

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

DefAntiDico(antidicpath)

# print(anti_dico)

general_dico = {}

voc_dictionnary = defaultdict(lambda: 0)

def DicoFromFiles(infolder):
    for filename in os.listdir(infolder) :
        if filename not in general_dico:
            dico = defaultdict(lambda: 0)
            fileHandler = open(infolder + filename, "r")
            lines = fileHandler.readlines()
            stemmer = PorterStemmer()
            for line in lines :
                line = line.lower()
                line = str.rstrip(line)
                racine = stemmer.stem(line)
                if anti_dico[racine] == 1 :
                    continue
                elif (racine in dico):
                    dico[racine] = dico[racine] + 1
                else :
                    dico[racine] = 1
                    # voc_dictionnary[racine] = 0

            general_dico[filename] = dico

            already_seen = []

            for line in lines :
                line = line.lower()
                line = str.rstrip(line)
                racine = stemmer.stem(line)
                if (racine not in already_seen):
                    if (dico[racine] > 0):
                        voc_dictionnary[racine] += 1
                        already_seen.append(racine)
            
            fileHandler.close()

DicoFromFiles(inpath)

# print(general_dico)

def saveJson(outpath, dictionary):
    dicoJson = json.dumps(dictionary, sort_keys=True, indent=4)
    fileJson = open(outpath + ".json", "w")
    fileJson.write(dicoJson)
    fileJson.close()

saveJson(outpath+"vocabulaire", voc_dictionnary)

N = len(voc_dictionnary)

for word in voc_dictionnary:
    voc_dictionnary[word] = math.log(N/(voc_dictionnary[word]))

saveJson(outpath+"vocabulaire", voc_dictionnary)

# QUESTION 5

def tf(filename):
    dico = {}
    fileHandler = open(filename, "r")
    lines = fileHandler.readlines()
    stemmer = PorterStemmer()
    for line in lines :
        line = line.lower()
        line = str.rstrip(line)
        racine = stemmer.stem(line)
        if anti_dico[racine] == 1 :
            continue
        elif (racine in dico):
            dico[racine] = dico[racine] + 1
        else :
            dico[racine] = 1
    fileHandler.close()
    return(dico)
    
vectorial_rep_dico = {}

def RepresentationVectorielle(infolder):
    fileJson = open("vocabulaire.json", "r")
    df = json.load(fileJson)
    for filename in os.listdir(infolder):
        dico_tf = tf(infolder+filename)
        for i in dico_tf:
            dico_tf[i] = dico_tf[i] * df[i]
        vectorial_rep_dico[filename] = dico_tf
    fileJson.close()
    # Sauvegarde de la représentation vectorielle dans un fichier
    return(vectorial_rep_dico)

RepresentationVectorielle(inpath)

# Sauvegarde de la représentation vectorielle dans un fichier
saveJson(outpath+"representation_vectorielle", vectorial_rep_dico)

# QUESTION 6

inv_index_dico = {}

def IndexInverse(infolder):
    fileJson = open("vocabulaire.json", "r")
    df = json.load(fileJson)
    for filename in os.listdir(infolder):
        dico_tf = tf(infolder+filename)
        for i in dico_tf:
            dico_tf[i] = dico_tf[i] * df[i]
        vectorial_rep_dico[filename] = dico_tf
    
    for word in df:
        inv_index_dico[word] = {}

    for word, idf in df.items():
        for filename, dico in vectorial_rep_dico.items():
            if word in dico:
                inv_index_dico[word][filename] = vectorial_rep_dico[filename][word]
    
    fileJson.close()
    return inv_index_dico

IndexInverse(inpath)

# Sauvegarde de l'index inversé dans un fichier
saveJson(outpath+"index_inverse", inv_index_dico)

# QUESTION 7

norme = {}

def Norme():
    fileJson = open("representation_vectorielle.json", "r")
    rv = json.load(fileJson)

    for filename, dico in rv.items():
        for word in dico:
            if filename in norme:
                norme[filename] += pow(rv[filename][word], 2)
            else:
                norme[filename] = pow(rv[filename][word], 2)

    for elem in norme:
        norme[elem] = numpy.sqrt(norme[elem])
    
    fileJson.close()
    return(norme)

Norme()

# Sauvegarde de la norme dans un fichier
saveJson(outpath+"norme", norme)
