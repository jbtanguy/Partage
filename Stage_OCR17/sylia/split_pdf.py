import PyPDF2 as pdf

pdf_file = open('/home/kecili100/Bureau/Partage/Stage_OCR17/sylia/mazarinades/mazarinade1.pdf','rb')
read_file = pdf.PdfFileReader(pdf_file) #the file object that has been read

num_pages = read_file.numPages

wrote_pdf = pdf.PdfFileWriter() #the file object which is to be written

for pageNum in range(2,num_pages-1):
    pageObj = read_file.getPage(pageNum)
    wrote_pdf.addPage(pageObj)

output_pdf = open('/home/kecili100/Bureau/Partage/Stage_OCR17/sylia/mazarinades/mazarinadeited.pdf','wb')

wrote_pdf.write(output_pdf)
output_pdf.close()
pdf_file.close()
