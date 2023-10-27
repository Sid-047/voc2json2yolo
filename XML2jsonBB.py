import xml.etree.ElementTree as ET
from colorama import Fore, Style
from tkinter import filedialog
from tqdm import tqdm
import pprint
import glob

print(Fore.YELLOW+Style.BRIGHT+"\n\nSelect in-XML-Content Directory"+Fore.RESET)
inDir = filedialog.askdirectory()

clsSet = set()
fileSet = set()
files = glob.glob(inDir+"/*.xml")
for f in tqdm(files, desc = "Fetching Class Names Yo!"):
    tree = ET.parse(f)
    root = tree.getroot()
    fileElement = root.find('filename')
    sizeElement = root.find('size')
    widthElement = sizeElement.find('width')
    heightElement = sizeElement.find('height')
    fileList = [fileElement.text, int(widthElement.text), int(heightElement.text)]
    fileSet.add(str((fileList)))
    for i in root.iter('name'):
        clsSet.add(i.text)

clsList = list(clsSet)
fileList = list(fileSet)
clsList.sort()

catList = []
imgList = []

for i in range(0, len(clsList)-1):
    dataDict = {}
    dataDict["id"] = i
    dataDict["name"] = clsList[i]
    dataDict["supercategory"] = "none"
    catList.append(dataDict)
    dataDict = {}

pprint.pprint(catList)

for j in range(0, len(fileList)-1):
    dataDict = {}
    dataList = eval(fileList[j])
    dataDict["id"] = j
    dataDict["file_name"] = dataList[0]
    dataDict["width"] = dataList[1]
    dataDict["height"] = dataList[2]
    imgList.append(dataDict)
    dataDict = {}

pprint.pprint(imgList)