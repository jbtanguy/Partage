
from pathlib import Path
from PIL import Image
import os

inputPath = Path(r"/home/kecili100/git/Partage/Stage_OCR17/sylia/jpg3")
inputFiles = inputPath.glob("**/*.jpg")
outputPath = Path("/home/kecili100/git/Partage/Stage_OCR17/sylia/png3")
os.mkdir(outputPath)
for f in inputFiles:
    outputFile = outputPath / Path(f.stem + ".png")
    im = Image.open(f)
    im.save(outputFile)
