import io
import os
import sys
import json
from nltk import ngrams

# 1. On récupère les trigrammes et leur fréquence du corpus de référence
path_tri_freq_ref = sys.argv[1]
with open('./trigrams_n_freq__corpus_ref/trigrammes_freq_corpus_SG.json') as json_file:
    trigrams_n_freq = json.load(json_file)

# 2. On met dans la liste files tous les chemins d'accès aux fichiers textes de notre corpus.
paths =[]
for file in os.listdir ("./ocr_results"):
	if file.endswith(".txt"): # Uniquement les fichiers finissant pas .txt
		paths.append(os.path.join("./ocr_results", file))


# 3. Créer un dictionnaire qui contient les textes (clef = path vers le fichier, valeur = son contenu (texte))
dic = {}
for path in paths:
	inFile = io.open(path, mode='r', encoding='utf-8') 
	txt = inFile.read() # récupération de contenue de fichier (string)
	trigrams_tuple = ngrams(txt, 3)
	trigrams = [''.join(elm) for elm in trigrams_tuple]
	dic[path] = trigrams

# 4. Associer un métrique d'évaluation à chaque txt résultat d'OCR 
# métrique : 1. somme des proba
#            2. moyenne des proba (moyenne et somme / nb total de proba)
for path, trigrams in dic.items():
	if len(trigrams) != 0:
		sum_proba = sum([trigrams_n_freq[t] for t in trigrams if t in trigrams_n_freq.keys()])
		mean_proba = sum([trigrams_n_freq[t] for t in trigrams if t in trigrams_n_freq.keys()]) / len(trigrams)
		print(path + '\t' + str(sum_proba) + '\t' + str(mean_proba))
	else:
		print(path + '\t' + str(0) + '\t' + str(0))