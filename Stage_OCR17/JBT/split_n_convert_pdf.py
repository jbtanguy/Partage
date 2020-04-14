import glob
from pdf2image import convert_from_path

path_to_pdf_dir = './pdf/' # Ici tu mets le chemin vers le dossier qui contient les pdfs
path_to_jpg_dir = './jpg/' # Ici tu mets le chemin vers le dossier qui contienDRA les jpgs
path_to_pdf_list = glob.glob(path_to_pdf_dir + '*pdf') # '*pdf' = ne considère que les fichiers .pdf du dossier


for path_to_pdf in path_to_pdf_list: # Pour tous les pdf du dossier <path_to_pdf_dir>
    # path_to_pdf : chemin vers un pdf du dossier 
    root_name_pdf = path_to_pdf.split('/')[-1].split('.')[0] # pour un path comme './pdf/1564865.pdf', ça donne '1564865'
    root_name_jpg = path_to_jpg_dir + root_name_pdf # ça donne : './jpg/' + '1564865'
    
    pages = convert_from_path(path_to_pdf, dpi=400) # On récupère dans une liste d'un ensemble d'Image (librairie PIL)
    for idx, page in enumerate(pages):
    	if idx >= 2: # Avec cette condition, on ne prend pas en compte les deux premières pages générées par Gallica
    		page.save(root_name_jpg+str(idx)+'.jpg', 'JPEG')

    pages = [] # Nécessaire, sinon le processus est arrêté avec seulement "Processus arrêté" comme info dans le Terminal