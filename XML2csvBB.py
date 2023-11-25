import xml.etree.ElementTree as ET
from colorama import Fore, Style
from tkinter import filedialog
from tqdm import tqdm
import glob
import csv

print(Fore.YELLOW+Style.BRIGHT+"\n\nSelect in-XML-Content Directory"+Fore.RESET)
inDir = filedialog.askdirectory()
print(Fore.CYAN+Style.BRIGHT+"\n\nand Come On! Select outPut CSV Directory"+Fore.RESET)
outDir = filedialog.askdirectory() + '\\'

csvTrainData = [['filename', 'width', 'height', 'class', 'xmin', 'ymin', 'xmax', 'ymax']]
csvTestData = [['filename', 'width', 'height', 'class', 'xmin', 'ymin', 'xmax', 'ymax']]
csvData = [['filename', 'width', 'height', 'class', 'xmin', 'ymin', 'xmax', 'ymax']]
files = glob.glob(inDir+"/*.xml")
dataNum = len(files)
trainNum = round(dataNum*0.8)
for f in tqdm(files[:trainNum], desc = "Gettin' the trainCSV File out Yo!"):
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
        csvTrainData.append(labelData)
        csvData.append(labelData)

for f in tqdm(files[:trainNum], desc = "Gettin' the testCSV File out Yo!"):
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


        xMin = int(float(bbxElement.find('xmin').text))
        yMin = int(float(bbxElement.find('ymin').text))
        xMax = int(float(bbxElement.find('xmax').text))
        yMax = int(float(bbxElement.find('ymax').text))

        labelData.extend([imgName, imgWidth, imgHeight, clsName, xMin, yMin, xMax, yMax])
        csvTrainData.append(labelData)
        csvData.append(labelData)

outFile = outDir + 'completeLabels.csv'
f = open(outFile, 'w')
csvWriter = csv.writer(f)
for row in tqdm(csvData, desc = "Writin' completeLabels Yo!", colour = "red"):
    csvWriter.writerow(row)
f.close()

outFile = outDir + 'train_labels.csv'
f = open(outFile, 'w')
csvWriter = csv.writer(f)
for row in tqdm(csvTrainData, desc = "Writin' trainLabels Yo!", colour = "red"):
    csvWriter.writerow(row)
f.close()

outFile = outDir + 'test_labels.csv'
f = open(outFile, 'w')
csvWriter = csv.writer(f)
for row in tqdm(csvTestData, desc = "Writin' testLabels Yo!", colour = "red"):
    csvWriter.writerow(row)
f.close()