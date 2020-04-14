import glob
import io
from pdf2image import convert_from_path
import pytesseract as pt 
from PIL import Image 

def write_ocr_result(file_path, ocr_result):
	outFile = io.open(file_path, mode='w', encoding='utf-8')
	outFile.write(ocr_result)
	outFile.close()
	print(file_path + ' : done.')

path_to_pdf_dir = './pdf/' # Ici tu mets le chemin vers le dossier qui contient les pdfs
path_to_jpg_dir = './jpg/' # Ici tu mets le chemin vers le dossier qui contienDRA les jpgs
path_to_txt_dir = './txt/' # Ici tu mets le chemin vers le dossier qui contienDRA les textes
path_to_pdf_list = glob.glob(path_to_pdf_dir + '*pdf') # '*pdf' = ne considère que les fichiers .pdf du dossier


for path_to_pdf in path_to_pdf_list: # Pour tous les pdf du dossier <path_to_pdf_dir>
    # path_to_pdf : chemin vers un pdf du dossier 
    root_name_pdf = path_to_pdf.split('/')[-1].split('.')[0] # pour un path comme './pdf/1564865.pdf', ça donne '1564865'
    root_name_jpg = path_to_jpg_dir + root_name_pdf # ça donne : './jpg/' + '1564865'
    root_name_txt = path_to_txt_dir + root_name_pdf

    pages = convert_from_path(path_to_pdf, dpi=400) # On récupère dans une liste d'un ensemble d'Image (librairie PIL)
    for idx, page in enumerate(pages):
    	if idx >= 2: # Avec cette condition, on ne prend pas en compte les deux premières pages générées par Gallica
    		img_path = root_name_jpg + str(idx) + '.jpg'
    		page.save(img_path, 'JPEG')
    		img = Image.open(img_path) 
    		txt = pt.image_to_string(img, lang="eng")
    		txt_path = root_name_txt + str(idx) + '.txt'
    		write_ocr_result(file_path=txt_path, ocr_result=txt)

    pages = [] # Nécessaire, sinon le processus est arrêté avec seulement "Processus arrêté" comme info dans le Terminal