import os
from operator import itemgetter
import math

dico = {}

def Zipf(infile):
    fileHandler = open("collection_tokens/"+infile, "r")
    lines = fileHandler.readlines()
    for line in lines:
        words = line.split()
        for word in words:
            if (word.lower() in dico):
                dico[word] += 1
            else:
                dico[word] = 1
    fileHandler.close()
    
directory = "/home/eve/Documents/4A/S8/MRI/TP1/collection_tokens/"
    
for filename in os.listdir(directory):
    Zipf(filename)
    
print("Affichage du dictionnaire de mots avec leurs nombres d'occurences :")

print (dico)

# QUESTION 3 partie 2
# print("Affichage des mots avec leurs nombres d'occurences par ordre décroissant d'occurences:")
    
# for word in reversed(sorted(dico.items(), key = itemgetter(1))):
#      print (word)


# QUESTION 4

cmp = 0

# Affichage des 10 mots les plus fréquents et leurs fréquences

for word in reversed(sorted(dico.items(), key = itemgetter(1))):
    print (word)
    print ("Le lambda de '" + word[0] + "' est " + str((word[1])/math.log(len(dico))))
    cmp += 1
    if (cmp > 9):
        break
    
# Taille du vocabulaire

print("Le dictionnaire contient " + str(len(dico)) + " mots")






    