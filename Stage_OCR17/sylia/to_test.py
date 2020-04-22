import glob
import io # to acess files and streams
import os

from pdf2image import convert_from_path
import pytesseract as pt 
from PIL import Image 



path_to_pdf_dir = r'/home/kecili100/git/Partage/Stage_OCR17/sylia/pdf/'
print (path_to_pdf_dir)
path_to_png_dir = '/home/kecili100/git/Partage/Stage_OCR17/sylia/pngs/'  
os.mkdir (path_to_png_dir) 
path_to_pdf_list = glob.glob(path_to_pdf_dir + '*pdf')
for path_to_pdf in path_to_pdf_list: 
    root_name_pdf = path_to_pdf.split('/')[-1].split('.')[0] 
    root_name_png = path_to_png_dir + root_name_pdf 
    pages = convert_from_path(path_to_pdf, dpi=200) 
    for page in (pages):
        img_path = root_name_png +'image' + '.png'
        print (img_path)
        page.save(img_path, 'PNG')
        img = Image.open(img_path, 'r')
        img1 = Image.Image.getcolors(img)
        print(img1)
        continue
            
