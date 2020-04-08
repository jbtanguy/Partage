from PIL import Image
import cv2
import pytesseract as pt
import os

      
def main():
    # path for the folder for getting the raw images
    path = './jpg3'
  
    # path for the folder for getting the output
    tempPath = './txt3'
  
    # iterating the images inside the folder
    for imageName in os.listdir(path):
	

        inputPath = os.path.join(path, imageName)
        img = Image.open(inputPath)
        # applying ocr using pytesseract for python
        text = pt.image_to_string(img, lang="fra")
  
        
        imagePath = inputPath[0:-4]
  
        fullTempPath = os.path.join(tempPath, 'edited'+imageName+".txt")
    
        # saving the  text for every image in a separate .txt file
        file1 = open(fullTempPath, "w")
        file1.write(text)
        file1.close()
  
if __name__ == '__main__':
    main()
