import sys
import io
import json
from nltk import ngrams


# 1. Récupération du contenu textuel du corpus de référence
path_corpus_ref = sys.argv[1]
inFile = io.open(path_corpus_ref, mode='r', encoding='utf-8') 
txt = inFile.read().replace('\n', ' ').replace('  ', ' ').lower() # récupération de contenue de fichier (string) + suppression des retours chariots et des doubles espaces + on met en minuscule

# 2. Récupération des trigrammes et de leur fréquence dans ce corpus de référence
n = 3
trigrams_tuple = ngrams(txt, n)
trigrams = [''.join(elm) for elm in trigrams_tuple] # compréhension de liste (--> dedans, l'ensemble des trigrammes du corpus de ref)
#print(len(txt))
#print(len(trigrams))
#print(len(set(trigrams)))

dic_trigrams = {} #clef: trigram, valeur: fréquence du trigramme (qu'on considèrera comme une proba)
dic_trigrams = {t: trigrams.count(t)/len(trigrams) for t in set(trigrams)} # compréhension de dictionnaire (dedans, clef = un trigramme, valeur = sa fréquence dans le corpus de réf)

# 3. On sauve le dictionnaire de trigramme-fréquence dans un fichier json
with io.open('./trigrams_n_freq__corpus_ref/trigrammes_freq_corpus_SG.json', mode='w', encoding='utf-8') as outFile: # Dans le dossier "trigrams_n_freq__corpus_ref" on va créer un fichier 
#"trigrammes_freq_corpus_SG.json" pour mettre nos résultats.
	json.dump(dic_trigrams, outFile, indent=4)