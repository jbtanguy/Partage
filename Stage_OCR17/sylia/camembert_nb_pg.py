
from os import listdir
from os.path import isfile, join
from PyPDF2 import PdfFileReader
import matplotlib.pylab as plt

#une foction qui récupère le contenu de corpus 

def getFolderContent(path):
  onlyPdfFiles = [f for f in listdir(path) if isfile(join(path, f)) and  f.endswith(".pdf")]
  return onlyPdfFiles
#pour récupérer le nombre de pages d'un fichhier

def nbrPDF(file):
  pdf = PdfFileReader(open(file,'rb'))
  return pdf.getNumPages()
path='./../pdf/'

files=getFolderContent(path)


# regrouper les fichiers selon le nombre de pages


from itertools import groupby
def projection(val):
    return val // 2

def getPageSorted(files):
  dictionary={}
  page=[nbrPDF(path+file) for file in files]
  page_sorted = sorted(page, key=projection)
  return page_sorted

def getGroupedPage(page_sorted):
  page_grouped = [list(it) for k, it in groupby(page_sorted, projection)]
  return page_grouped

def getRegroupedPage(page_grouped):
  dic={}
  for s in page_grouped:
       n=max(s)
       n=n + (10 - n % 10)
       dic[n]=len(s)
  return dic


dic=getPageSorted(files)
print('le nombre de page pour chaque pdf')
print(dic)
dic=getGroupedPage(dic)
print("nombre de page regrouper")
print(dic)
dic=getRegroupedPage(dic)
print("regrouped pages ")
print(dic)

plt.subplots(figsize=(20,10))
lists = sorted(dic.items()) # sorted by key, return a list of tuples
plt.pie([float(v) for v in dic.values()] ,
autopct='%2.2f%%', shadow=True, startangle=140)
plt.legend(labels=["page< "+str(k) + " " +str(dic[k])for k in dic], bbox_transform=plt.gcf().transFigure,fontsize=30, loc="best")

plt.axis('equal')
plt.show()



