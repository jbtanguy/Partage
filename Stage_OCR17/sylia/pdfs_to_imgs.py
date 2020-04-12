from pdf2image import convert_from_path 
import os
import glob

path = r'/home/kecili100/Bureau/Partage/Stage_OCR17/kecili/mazarinades_net'
liste= glob.glob("*.pdf")
for element in liste:
    pages= convert_from_path(element)
    print (len (pages))
    i=1
    for page in pages:
        page.save(element + str (i)+ ".jpg")
        print ((element + str (i)+ ".jpg"))
        print (i)
        i=i+1
