import os
from nltk.tokenize import RegexpTokenizer

tokenizer = RegexpTokenizer('[A-Za-z]{1,}')

def TokenizeFile(infile, outpath):
    fileHandler = open("collection/"+infile, "r")
    f = open(outpath+infile+".flt", "w+")
    while True:
        line = fileHandler.readline()
        if not line:
            break
        words = tokenizer.tokenize(line)
        for word in words:
            f.write(word.lower()+"\n")
    fileHandler.close()
    f.close()

outpathname = "/home/eve/Documents/4A/S8/MRI/TP1/collection_tokens/"
directory = "/home/eve/Documents/4A/S8/MRI/TP1/collection/"

for filename in os.listdir(directory):
    TokenizeFile(filename, outpathname)
