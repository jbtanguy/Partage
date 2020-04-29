import glob
import io # to acess files and streams
import os
from pdf2image import convert_from_path
import pytesseract as pt 
from PIL import Image 
from optparse import OptionParser

def write_ocr_result(file_path, ocr_result):
    outFile = io.open(file_path, mode='w', encoding='utf-8')
    outFile.write(ocr_result)
    outFile.close()
    print(file_path + ' : done.')

if __name__ == "__main__":

    # Options parsing
    """
    parser = OptionParser()
    parser.add_option("-c", "--corpusdir", dest="corpusdir",
                      help="path to the pdf corpus")
    parser.add_option("-i", "--imgdir", dest="imgdir",
                      help="path to the directory where to store the generated images")
    parser.add_option("-t", "--txtdir", dest="txtdir",
                      help="path to the directory where to store the generated texts (OCR results)")
    parser.add_option("-d", "--dpi", dest="dpi",
                      help="dpi (int)")
    (options, args) = parser.parse_args()
    path_to_pdf_dir = options.corpusdir
    path_to_png_dir = options.imgdir
    path_to_txts_dir = options.txtdir
    dpi = options.dpi
    """

    path_to_pdf_dir = './../corpora/get_pdfs_from_gallica/corpus/mazarinades/pdf/' 
    path_to_png_dir = './../JBT/png/'
    path_to_txts_dir = './../JBT/txt/'
    dpi = 300
    path_to_pdf_list = glob.glob(path_to_pdf_dir + '*pdf') 


    for path_to_pdf in path_to_pdf_list: 
        root_name_pdf = path_to_pdf.split('/')[-1].split('.')[0] 
        root_name_png = path_to_png_dir + root_name_pdf
        root_name_txts = path_to_txts_dir + root_name_pdf

        pages = convert_from_path(pdf_path=path_to_pdf, dpi=dpi) # Conversion du PDF courant en une liste d'images
        for idx, img in enumerate(pages): # parcours de toutes les images 
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
        pages = []