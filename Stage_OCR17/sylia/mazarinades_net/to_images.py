from pdf2image import convert_from_path 
import os
import glob

path = r'/home/kecili100/git/Partage/Stage_OCR17/sylia/mazarinades_net'
liste= glob.glob("*.pdf")
dir_images = "/home/kecili100/git/Partage/Stage_OCR17/sylia/mazarinades_jpg/"
os.mkdir(dir_images)
for element in liste:
    pages= convert_from_path(element)
    #print (len (pages))
    i=1
    for page in pages:
        page.save(dir_images+ element + str (i)+ ".jpg")
        #print ((element + str (i)+ ".jpg"))
        #print (i)
        i=i+1

####
