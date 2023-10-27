import xml.etree.ElementTree as ET
from colorama import Fore, Style
from tkinter import filedialog
from tqdm import tqdm
import pprint
import glob

print(Fore.YELLOW+Style.BRIGHT+"\n\nSelect in-XML-Content Directory"+Fore.RESET)
inDir = filedialog.askdirectory()

clsSet = set()
files = glob.glob(inDir+"/*.xml")
for f in tqdm(files, desc = "Fetching Class Names Yo!"):
    tree = ET.parse(f)
    root = tree.getroot()
    for i in root.iter('name'):
        clsSet.add(i.text)

clsList = list(clsSet)
clsList.sort()

catList = []

for i in range(0, len(clsList)-1):
    dataDict = {}
    dataDict["id"] = i
    dataDict["name"] = clsList[i]
    dataDict["superctaegory"] = "none"
    catList.append(dataDict)
    dataDict = {}

pprint.pprint(catList)