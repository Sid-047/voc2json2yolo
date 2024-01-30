import xml.etree.ElementTree as ET
from colorama import Fore, Style
from tkinter import filedialog
from tqdm import tqdm
import glob

print(Fore.YELLOW+Style.BRIGHT+"\n\nSelect in-segXML-Content Directory"+Fore.RESET)
inDir = filedialog.askdirectory()
print(Fore.CYAN+Style.BRIGHT+"\n\nand Come On! Select outPut polyXML Directory"+Fore.RESET)
outDir = filedialog.askdirectory()
if "\\" in outDir:
    outDir = outDir + '\\'
else:
    outDir = outDir + '/'

files = glob.glob(inDir+"/*.xml")
for f in tqdm(files, desc = "Processing Stuff!"):
    f_ = f.replace("\\", "~").replace("/", "~")
    outFile = f_.split("~")[-1]
    outFile = outDir + outFile
    print(outFile)
    tree = ET.parse(f)
    root = tree.getroot()

    pathElement = root.find('path')
    if pathElement is not None:
        pathElement.text = '..//'+root.findtext('folder')+'//'+root.findtext('filename')
    sourceElement = root.find('source')
    if sourceElement is not None:
        root.remove(sourceElement)

    objectElements = root.findall('object')
    for objectElement in objectElements:
        pnts = []
        for i in objectElement.iter('value'):
            pnts.append(i.text)

        if len(pnts)%2==0:
            a = [x for x in pnts[::2]]
            b = [y for y in pnts[1::2]]
            pnts = list(zip(a,b))
            pntSet = set(pnts)
            pnts = list(pntSet)
        else:
            pnts.pop()
            a = [x for x in pnts[::2]]
            b = [y for y in pnts[1::2]]
            pnts = list(zip(a,b))
            pntSet = set(pnts)
            pnts = list(pntSet)

        segmentationElement = objectElement.find('segmentations')
        objectElement.remove(segmentationElement)

        polygonElement = ET.Element("polygon")
        for val, j in enumerate(pnts, start = 1):
            xPnt = ET.Element("x"+str(val))
            xPnt.text = j[0]
            yPnt = ET.Element("y"+str(val))
            yPnt.text = j[1]
            polygonElement.append(xPnt)
            polygonElement.append(yPnt)

        objectElement.append(polygonElement)

        xmlString = ET.tostring(objectElement, encoding='utf8').decode('utf8')
    tree.write(outFile)