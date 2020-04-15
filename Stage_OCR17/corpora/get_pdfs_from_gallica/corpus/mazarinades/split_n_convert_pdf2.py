import glob
import io
import os
from pdf2image import convert_from_path
import pytesseract as pt 
from PIL import Image 

def write_ocr_result(file_path, ocr_result):
	outFile = io.open(file_path, mode='w', encoding='utf-8')
	outFile.write(ocr_result)
	outFile.close()
	print(file_path + ' : done.')

path_to_pdf_dir = r'/home/kecili100/git/Partage/Stage_OCR17/corpora/get_pdfs_from_gallica/corpus/mazarinades/pdf/' 
path_to_jpg_dir = '/home/kecili100/git/Partage/Stage_OCR17/corpora/get_pdfs_from_gallica/corpus/mazarinades/jpg/'  
os.mkdir (path_to_jpg_dir)
path_to_txt_dir = '/home/kecili100/git/Partage/Stage_OCR17/corpora/get_pdfs_from_gallica/corpus/mazarinades/txt/' 
os.mkdir (path_to_txt_dir)
path_to_pdf_list = glob.glob(path_to_pdf_dir + '*pdf') 


for path_to_pdf in path_to_pdf_list: 
    
    root_name_pdf = path_to_pdf.split('/')[-1].split('.')[0] 
    root_name_jpg = path_to_jpg_dir + root_name_pdf 
    root_name_txt = path_to_txt_dir + root_name_pdf

    pages = convert_from_path(path_to_pdf, dpi=400) 
    for idx, page in enumerate(pages):
    	if idx >= 2:

    		img_path = root_name_jpg + str(idx) + '.jpg'
    		page.save(img_path, 'JPEG')
    		img = Image.open(img_path) 
    		txt = pt.image_to_string(img, lang="eng")
    		txt_path = root_name_txt + str(idx) + '.txt'
    		write_ocr_result(file_path=txt_path, ocr_result=txt)

    pages = []
