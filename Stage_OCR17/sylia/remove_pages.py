import PyPDF2 as pdf
import glob
import os
# Supprimer les deux premières pages dans tout les fichiers pdfs

pdf_directory_name = "/../pdf/"
pdf_files_list= glob.glob(pdf_directory_name + '*pdf')
pdf_net_directory="/../pdf_net/"
os.mkdir(pdf_net_directory)
for pdf_file in pdf_files_list:
 

   based_file_name = open(pdf_file ,'rb')
   read_file = pdf.PdfFileReader(pdf_file) #the file object that has been read
   print (pdf_file)
   based_file_name= os.path.splitext(os.path.basename(pdf_file ))[0]
   num_pages = read_file.numPages

   wrote_pdf = pdf.PdfFileWriter() #the file object which is to be written

   for pageNum in range(2,num_pages-1):
       pageObj = read_file.getPage(pageNum)
       wrote_pdf.addPage(pageObj)

   with open(pdf_net_directory+ based_file_name+'Edited.pdf','wb')as file: 
    

       wrote_pdf.write(file)
       file.close()
       file.close()
