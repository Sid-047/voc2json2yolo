
import xml.etree.ElementTree as ET
from colorama import Fore, Style
from tkinter import filedialog
from PIL import Image
from tqdm import tqdm
import glob
import os

print(Fore.YELLOW+Style.BRIGHT+"\n\nSelect in-XML-Content Directory"+Fore.RESET)
inXmlDir = filedialog.askdirectory()
print(Fore.BLUE+Style.BRIGHT+"\n\nSelect the in-IMG-Content Directory"+Fore.RESET)
imgDir = filedialog.askdirectory() + '\\'
print(Fore.CYAN+Style.BRIGHT+"\n\nand Come On! Select outPut Directory"+Fore.RESET)
outDir = filedialog.askdirectory() + '\\'

clsSet = set()
files = glob.glob(inXmlDir+"/*.xml")
for f in tqdm(files, desc = "Fetching Class Names Yo!"):
    tree = ET.parse(f)
    root = tree.getroot()
    for i in root.iter('name'):
        clsSet.add(i.text)

clsList = list(clsSet)
clsList.sort()
print(clsList)

for i in clsList:
    outFolder = outDir + i
    if not os.path.isdir(outFolder):
        os.makedirs(outFolder)

c = 0
for f in tqdm(files, desc = "Flowin' through the Images Yo!", colour = "red"):
    try:
        imgFile = imgDir + (f.split("\\")[-1]).split('.')[0] + '.jpg'
        imgObj = Image.open(imgFile)
    except:
        try:
            imgFile = imgDir + (f.split("\\")[-1]).split('.')[0] + '.png'
            imgObj = Image.open(imgFile)
        except:
            imgFile = imgDir + (f.split("\\")[-1]).split('.')[0] + '.tiff'
            imgObj = Image.open(imgFile)

    tree = ET.parse(f)
    root = tree.getroot()
    
    c = 0
    objectElements = root.findall('object')
    for objectElement in tqdm(objectElements, desc = "Gettin' the Class Objects out Yo!"):
        nameElement = objectElement.find('name')
        clsName = nameElement.text
        bbxElement = objectElement.find('bndbox')
        xMin = int(float(bbxElement.find('xmin').text))
        yMin = int(float(bbxElement.find('ymin').text))
        xMax = int(float(bbxElement.find('xmax').text))
        yMax = int(float(bbxElement.find('ymax').text))
        try:
            cropImg = imgObj.crop((xMin, yMin, xMax, yMax))
            outFolder = outDir + clsName + '\\'
            cropImg.save(outFolder + clsName + str(c) + '.jpg')
            c+=1
        except:
            pass