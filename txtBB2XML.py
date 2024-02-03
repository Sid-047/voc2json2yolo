import xml.etree.ElementTree as ET
from colorama import Fore, Style
from tkinter import filedialog
from tqdm import tqdm
import glob
import os

print(Fore.YELLOW+Style.BRIGHT+"\n\nSelect in-TxT-Content Directory"+Fore.RESET)
inTxTDir = filedialog.askdirectory()
print(Fore.YELLOW+Style.BRIGHT+"\n\nSelect LabellediMG-Content Directory"+Fore.RESET)
inImGDir = filedialog.askdirectory()
print(Fore.BLUE+Style.BRIGHT+"\n\nSelect the numClasses Text File Yo!"+Fore.RESET)
inTxt = filedialog.askopenfilename(filetypes=[("NumClass TextFile", "*.txt")])
print(Fore.CYAN+Style.BRIGHT+"\n\nand Come On! Select outPut XML Directory"+Fore.RESET)
outDir = filedialog.askdirectory()
if "\\" in outDir:
    slashStuff = '\\'
else:
    slashStuff = '/'

f = open(inTxt, 'r')
clsNames = f.read().replace(", ", ',').split(',')
f.close()
clsDict = dict(zip(clsNames, list(range(len(clsNames)))))
print(clsDict)

files = glob.glob(inTxTDir+"/*.txt")
for f in tqdm(files, desc = "Gettin' the Txt File out Yo!"):
    f_ = f.replace("\\", "~").replace("/", "~")
    outName = (f_.split("~")[-1]).split('.')[0] + '.xml'
    if os.path.isfile(inImGDir + slashStuff + outName.replace(".xml", ".jpg")) or os.path.isfile(inImGDir + slashStuff + outName.replace(".xml", ".png")):
        outFile = outDir + slashStuff + outName
        print(outFile)
        txtFile = open(f, 'r')
        txtContents = txtFile.read().split('\n')
        txtFile.close()

        root = ET.Element("annotation")
        ET.SubElement(root, "folder").text = "images"
        ET.SubElement(root, "filename").text = outName.replace(".xml", ".jpg")
        ET.SubElement(root, "path").text = "..//images//{}".format(outName.replace(".xml", ".jpg"))
        
        
        sizeElement = ET.SubElement(root, "size")
