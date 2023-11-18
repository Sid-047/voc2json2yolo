import xml.etree.ElementTree as ET
from colorama import Fore, Style
from tkinter import filedialog
from tqdm import tqdm
import pprint
import glob
import csv

print(Fore.YELLOW+Style.BRIGHT+"\n\nSelect in-XML-Content Directory"+Fore.RESET)
inDir = filedialog.askdirectory()
print(Fore.CYAN+Style.BRIGHT+"\n\nand Come On! Select outPut CSV Directory"+Fore.RESET)
outDir = filedialog.askdirectory() + '\\'

csvData = [['filename', 'width', 'height', 'class', 'xmin', 'ymin', 'xmax', 'ymax']]
files = glob.glob(inDir+"/*.xml")
for f in tqdm(files, desc = "Gettin' the CSV File out Yo!"):
    outFile = outDir + "csvCompleteFile.csv"
    print(outFile)
    tree = ET.parse(f)
    root = tree.getroot()

    imgName = root.find('filename')
    sizeElement = root.find('size')
    widthElement = sizeElement.find('width')
    heightElement = sizeElement.find('height')
    imgWidth = int(widthElement.text)
    imgHeight = int(heightElement.text)
    
    labelData = []
    objectElements = root.findall('object')
    for objectElement in objectElements:
        nameElement = objectElement.find('name')
        clsName = nameElement.text
        bbxElement = objectElement.find('bndbox')
        xMin = int(float(bbxElement.find('xmin').text))
        yMin = int(float(bbxElement.find('ymin').text))
        xMax = int(float(bbxElement.find('xmax').text))
        yMax = int(float(bbxElement.find('ymax').text))

        labelData.extend([imgName, imgWidth, imgHeight, clsName, xMin, yMin, xMax, yMax])
        csvData.append(labelData)

f = open(outFile, 'w')
csvWriter = csv.writer(f)
csvWriter.writerows(csvData)
pprint.pprint(csvData)
f.close()