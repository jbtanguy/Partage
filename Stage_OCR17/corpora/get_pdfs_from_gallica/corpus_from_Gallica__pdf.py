###IMPORTS
import csv, re, json, os, glob, sys
from bs4 import BeautifulSoup #pour parser les fichiers HTML

###FONCTIONS ET VARIABLES GLOBALBES
#Auteur du code : https://codereview.stackexchange.com/questions/147712/convert-an-integer-to-its-roman-numeral-equivalent
def convert_to_roman(number):
    """ Convert an integer to Roman
    >>> print(convert_to_roman(45))
    XLV """
    number = int(number)
    roman_numerals = []
    for numeral, value in ROMAN_NUMERAL_TABLE:
        count = number // value
        number -= count * value
        roman_numerals.append(numeral * count)

    return ''.join(roman_numerals)

ROMAN_NUMERAL_TABLE = [
    ("M", 1000), ("CM", 900), ("D", 500),
    ("CD", 400), ("C", 100),  ("XC", 90),
    ("L", 50),   ("XL", 40),  ("X", 10),
    ("IX", 9),   ("V", 5),    ("IV", 4),
    ("I", 1)
]

###CODE
#Prend en argument un fichier CSV de Données bibliographiques de la recherche 
# Plus d'infos : https://gallica.bnf.fr/blog/09012017/nouvelle-fonction-pour-gallica-le-rapport-de-recherche
file = sys.argv[1]

dossier = file.split(".")[-2]

erreurs = open("erreurs_%s.csv"%(dossier), "w")

with open(file, newline='') as csvfile :
    reader = csv.reader(csvfile, delimiter = ';', quotechar='|')
    next(reader) #On 'passe' les entêtes
    data = [r for r in reader]

    #On récupère la première colonne du fichier, qui correspond aux URL
    #que l'on parse pour récupérer l'identifiant ARK
    listeARK = [ligne[0].split("/")[-1] for ligne in data]
    if not os.path.exists("corpus/%s/pdf/"%dossier) :
        os.makedirs("corpus/%s/pdf/"%dossier)

    """Pour chaque ARK, on :
        - on génère l'url pour accéder au texte brut
        - on fait un wget pour enregistrer la page HTML
        - on parse le document HTML pour accéder au texte brut/avec les balises
    """
    cut = 0.1
    for index, ark in enumerate(listeARK) :
        if index == int((len(listeARK)*cut)) :
            print ("- Documents traités : " + str(index) + " -")
            cut+=0.1
        url = "https://gallica.bnf.fr/ark:/12148/%s/f1n36.pdf"%(ark)
        commande = "wget -q %s -O corpus/%s/pdf/%s.pdf"%(url, dossier, ark)
        os.system(commande)
