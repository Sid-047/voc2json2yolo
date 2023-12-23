import xml.etree.ElementTree as ET
from colorama import Fore, Style
from tkinter import filedialog
from tqdm import tqdm
import glob

print(Fore.YELLOW+Style.BRIGHT+"\n\nSelect in-segmentXML-Content Directory"+Fore.RESET)
inDir = filedialog.askdirectory()
print(Fore.BLUE+Style.BRIGHT+"\n\nSelect the numClasses Text File Yo!"+Fore.RESET)
inTxt = filedialog.askopenfilename(filetypes=[("NumClass TextFile", "*.txt")])
print(Fore.CYAN+Style.BRIGHT+"\n\nand Come On! Select outPut TXT Directory"+Fore.RESET)
outDir = filedialog.askdirectory() + '\\'

f = open(inTxt, 'r')
clsDict = eval(f.read())
f.close()

print(clsDict)
files = glob.glob(inDir+"/*.xml")


for f in tqdm(files, desc = "Gettin' the Txt File out Yo!"):
    outFile = (f.split("\\")[-1]).split('.')[0] + '.txt'
    outFile = outDir + outFile
    print(outFile)
    tree = ET.parse(f)
    root = tree.getroot()

    sizeElement = root.find('size')
    widthElement = sizeElement.find('width')
    heightElement = sizeElement.find('height')
    xDiv = int(widthElement.text)
    yDiv = int(heightElement.text)
    
    labelData = []
    objectElements = root.findall('object')
    for objectElement in objectElements:
        nameElement = objectElement.find('name')
        clsName = nameElement.text
        pnts = []
        for i in objectElement.iter('value'):
            pnts.append(i.text)

        if len(pnts)%2==0:
            a = [int(x)/xDiv for x in pnts[::2]]
            b = [int(y)/yDiv for y in pnts[1::2]]
            pnts = list(zip(a,b))
            pntSet = set(pnts)
            pnts = list(pntSet)
            odns = [str(float(w)) for z in pnts for w in z]
        else:
            pnts.pop()
            a = [int(x)/xDiv for x in pnts[::2]]
            b = [int(y)/yDiv for y in pnts[1::2]]
            pnts = list(zip(a,b))
            pntSet = set(pnts)
            pnts = list(pntSet)
            odns = [str(float(w)) for z in pnts for w in z]

        loadData = ' '.join([str(clsDict[clsName])] + odns)
        labelData.append(loadData)
    txtData = '\n'.join(labelData)
    f_ = open(outFile, 'w')
    f_.write(txtData)
    f_.close()

clsTxt = '\n'.join(list(clsDict.keys()))
f = open(outDir+'classes.txt', 'w')
f.write(clsTxt)
f.close()