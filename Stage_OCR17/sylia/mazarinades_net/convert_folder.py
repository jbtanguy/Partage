
from pdf2image import convert_from_path
import glob
import os, subprocess

path_dir = r"/home/kecili100/Bureau/Partage/Stage_OCR17/kecili/mazarinades_net"

for folder_files in glob.glob(path_dir +"/*.pdf"):
     #print (folder_files)
     #pdf_files =open (folder_files, 'r')
     #content= pdf_files.read()
     #pdf_files.close()
	net1.pdf+(p1+'.jpg')
	net2.pdf+(p2+'.jpg')
	pages = convert_from_path(folder_files, 300)
	compteur = 1
	for page in pages:
		path_out = "folder_files"+"_p"+str(compteur) + ".jpg"
		
		page.save(path_out(folder_files,'JPEG'))
		compteur += 1
		print (path_out)






