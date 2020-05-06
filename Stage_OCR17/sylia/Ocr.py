import glob
import io
import os
from pdf2image import convert_from_path
import pytesseract as pt 
from PIL import Image 
from os import listdir
from os.path import isfile, join


#suppression d'images vides et celles générées par Gallica"

def getFolderContent(path):
  onlyPdfFiles = [f for f in listdir(path) if isfile(join(path, f)) and  f.endswith(".pdf")]
  return onlyPdfFiles


def write_ocr_result(file_path, ocr_result):
	outFile = io.open(file_path, mode='w', encoding='utf-8')
	outFile.write(ocr_result)
	outFile.close()
	print(file_path + ' : done.')

path_to_pdf_dir = '.' # le chemin vers le dossier qui contient les pdfs

path_to_png_dir = 'png/'
if not os.path.exists(path_to_png_dir):
    os.makedirs(path_to_png_dir)



path_to_pdf_list =getFolderContent(path_to_pdf_dir)# glob.glob(path_to_pdf_dir + '*.pdf') # '*pdf' = ne considère que les fichiers .pdf du dossier

print(path_to_pdf_list)

from PIL import Image
import pytesseract
import numpy as np
import cv2

for path_to_pdf in path_to_pdf_list: # Pour tous les pdf du dossier <path_to_pdf_dir>
    # path_to_pdf : chemin vers un pdf du dossier 

    root_name_pdf = path_to_pdf.split('.')[0] # pour un path comme './pdf/1564865.pdf', ça donne '1564865'
    root_name_png = path_to_png_dir + root_name_pdf # ça donne : './png/' + '1564865'
    
    dpi=100
    pages = convert_from_path(path_to_pdf, dpi=100) # On récupère dans une liste d'un ensemble d'Image (librairie PIL)
    for idx, img in enumerate(pages): # parcours de toutes les images 
            if idx<2:
              continue # sauter deux premier page 
            img_path = root_name_png + '_' + str(idx) + '.png'
            print(img_path+" "+str( len (img.getcolors())))
            img.save(img_path, 'PNG', dpi=(dpi, dpi)) # sauvegarde de l'image (car il s'agit d'une donnée qu'on a créé)
            
    pages = [] # Nécessaire, sinon le processus est arrêté avec seulement "Processus arrêté" comme info dans le Terminal
print('fin de tache')








      
