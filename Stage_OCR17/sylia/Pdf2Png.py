# -*- coding: utf-8 -*-

import glob
import io
import os
from pdf2image import convert_from_path
import pytesseract as pt 
from PIL import Image 
from os import listdir
from os.path import isfile, join

def getFolderContent(path):
  onlyPdfFiles = [f for f in listdir(path) if isfile(join(path, f)) and  f.endswith(".pdf")]
  return onlyPdfFiles


path_to_png_dir = 'png/'
if not os.path.exists(path_to_png_dir):
    os.mkdir(path_to_png_dir)


path_to_pdf_dir= 'pdf_test/'
path_to_pdf_list = getFolderContent(path_to_pdf_dir) 
print(path_to_pdf_list)

from PIL import Image
import pytesseract
import numpy as np
import cv2


for path_to_pdf in path_to_pdf_list: # Pour tous les pdf du dossier <path_to_pdf_dir>
    # path_to_pdf : chemin vers un pdf du dossier 

    root_name_pdf = path_to_pdf.split('.')[0] # pour un path comme './pdf/1564865.pdf', ça donne '1564865'
    root_name_png = path_to_png_dir + root_name_pdf # ça donne : './png/' + '1564865'
    #root_name_txt=path_to_txt_dir+root_name_pdf
    dpi=300
    pages = convert_from_path(path_to_pdf_dir+path_to_pdf, dpi=300) # On récupère dans une liste d'un ensemble d'Image (librairie PIL)
    for idx, img in enumerate(pages): # parcours de toutes les images 
        #if idx in [0,1]:
            #continue # sauter deux premier page 
        if img.getcolors() != None:
            if len(img.getcolors()) == 256:
            #print(str(len(img.getcolors())))
               img_path = root_name_png + '_' + str(idx) + '.png'
               img.save(img_path, 'PNG', dpi=(dpi, dpi)) # sauvegarde de l'image (car il s'agit d'une donnée qu'on a créé)
 
    print(root_name_pdf)
    pages = [] # Nécessaire, sinon le processus est arrêté avec seulement "Processus arrêté" comme info dans le Terminal
print('fin de tache')


