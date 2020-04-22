import glob
import io # to acess files and streams
import os
from pdf2image import convert_from_path
import pytesseract as pt 
from PIL import Image 




def write_ocr_result(file_path, ocr_result):
	outFile = io.open(file_path, mode='w', encoding='utf-8')
	outFile.write(ocr_result)
	outFile.close()
	print(file_path + ' : done.')

path_to_pdf_dir = r'/home/kecili100/git/Partage/Stage_OCR17/sylia/pdf/' 
path_to_png_dir = '/home/kecili100/git/Partage/Stage_OCR17/sylia/pngs/'  
os.mkdir (path_to_png_dir)
path_to_txts_dir = '/home/kecili100/git/Partage/Stage_OCR17/sylia/txtes/' 
os.mkdir (path_to_txts_dir)
path_to_pdf_list = glob.glob(path_to_pdf_dir + '*pdf') 


for path_to_pdf in path_to_pdf_list: 
    
    root_name_pdf = path_to_pdf.split('/')[-1].split('.')[0] 
    root_name_png = path_to_png_dir + root_name_pdf 
    root_name_txts = path_to_txts_dir + root_name_pdf

    pages = convert_from_path(path_to_pdf, dpi=200) 
    for idx, page in enumerate(pages):
    	if idx >= 2:
                img_path = root_name_png + str(idx) + '.png'
                page.save(img_path, 'PNG')
                img = Image.open(img_path) 
                if len(img.getcolors()) < 2:
                   # print (len(img.getcolors()))
                    continue
                  
                txt_eng = pt.image_to_string(img, lang="eng")
                txt_fra = pt.image_to_string(img, lang="fra")
                txt_path_eng = root_name_txts + str(idx) + '_200dpi_pytesseract_eng.txt'
                txt_path_fra = root_name_txts + str(idx) + '-200dpi_pytesseract_fra.txt'
                write_ocr_result(file_path=txt_path_eng, ocr_result=txt_eng)
                write_ocr_result(file_path=txt_path_fra, ocr_result=txt_fra)
                # cmd = 'kraken -I "pngs/*.png" -o _benarized.png binarize'
                # os.system (cmd)

    pages = []
