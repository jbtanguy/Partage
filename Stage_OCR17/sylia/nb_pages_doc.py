
import PyPDF2 as pdf
import glob
from PyPDF2 import PdfFileWriter, PdfFileReader

import os, sys

directory_name = r'/home/kecili100/git/Partage/Stage_OCR17/sylia/pdf/' 

directory_name_list = glob.glob(directory_name + '*pdf')


for filename in directory_name_list:
    #print ('name: %s' % filename)

    output_file = PdfFileWriter()
    input_handle = open(filename, 'rb')
    input_file = PdfFileReader(input_handle)

    num_pages = input_file.getNumPages()

    print ('name: %s' % filename, "document has %s pages \n" % num_pages)



