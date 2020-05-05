import glob
import io
import os
from pdf2image import convert_from_path
import pytesseract as pt 
from PIL import Image 
from os import listdir
from os.path import isfile, join

def getFolderContent (path):
    onlyPdfFiles = [f for f in listdir(path) if isfile(join(path, f)) and  f.endswith(".pdf")]
    return onlyPdfFiles

def write_ocr_result(file_path, ocr_result):
	outFile = io.open(file_path, mode='w', encoding='utf-8')
	outFile.write(ocr_result)
	outFile.close()
	print(file_path + ' : done.')

path_to_pdf_dir = 'r/home/kecili100/git/Partage/Stage_OCR17/sylia/pdf_test/' # le chemin vers le dossier qui contient les pdfs

path_to_png_dir = '/home/kecili100/git/Partage/Stage_OCR17/sylia/png/' # le chemin vers le dossier qui contienDRA les pngs
os.mkdir(path_to_png_dir)
path_to_txt_dir = '/home/kecili100/git/Partage/Stage_OCR17/sylia/txt/' # le chemin vers le dossier qui contienDRA les textes
os.mkdir (path_to_txt_dir)
path_to_pdf_list = glob.glob(path_to_pdf_dir + '*pdf') # '*pdf' = ne considère que les fichiers .pdf du dossier

print (path_to_pdf_list)


for path_to_pdf in path_to_pdf_list: # Pour tous les pdf du dossier <path_to_pdf_dir>
    # path_to_pdf : chemin vers un pdf du dossier 
    root_name_pdf = path_to_pdf.split('/')[-1].split('.')[0] # pour un path comme './pdf/1564865.pdf', ça donne '1564865'
    root_name_png = path_to_png_dir + root_name_pdf # ça donne : './png/' + '1564865'
    root_name_txt = path_to_txt_dir + root_name_pdf # ça donne : './txt/' + '1564865'

    pages = convert_from_path(path_to_pdf, dpi=300) # On récupère dans une liste d'un ensemble d'Image (librairie PIL)
    for idx, img in enumerate(pages): # parcours de toutes les images 
        if idx<2:
            continue
        img_path = root_name_png + '_' + str(idx) + '.png'
        img.save(img_path, 'PNG', dpi=(dpi, dpi)) # sauvegarde de l'image (car il s'agit d'une donnée qu'on a créé)
            # La fonction .getcolors() nous permet de trier les pages des PDF correspondant à des numérisations de mazarinades de celles générées par Gallica, ou totalement ou presque vides
        if img.getcolors() != None:
                if len(img.getcolors()) > 70: # Les pages issues de numérisation compte 258 couleurs, alors que les générées n'en comptent que 68
    		# OCR with tesseract 4
                    for lang in ['eng', 'fra']:# Pour tous les modèles de langue qu'on souhaite utiliser
                        txt = pt.image_to_string(img, lang=lang) # OCR processing
                        path = '_'.join([root_name_txts, str(idx), str(dpi)+'dpi', 'tesseract', lang]) + '.txt' 
                        write_ocr_result(file_path=path, ocr_result=txt) # Sauvegarde dans un fichier .txt du résultat d'OCR
                        cmd = 'kraken -I \"' + work_dir + '*' + '.png' + '\" -o _binarized.png binarize'
                        os.system(cmd)
    
    # 3. OCR Kraken: model Simon Gabay
                        cmd = 'kraken -I \"' + work_dir + '*_binarized.png' + '\" -o _kraken_SG_model.txt segment ocr -m ./../kraken_models/kraken_CORPUS17_SimonGabay.mlmodel'
                        os.system(cmd)
    pages = [] # Nécessaire, sinon le processus est arrêté avec seulement "Processus arrêté" comme info dans le Terminal
