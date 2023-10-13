import xml.etree.ElementTree as ET
from colorama import Fore, Style
from tkinter import filedialog
from tqdm import tqdm
import glob

print(Fore.YELLOW+Style.BRIGHT+"\n\nSelect in-Content Directory"+Fore.RESET)
inDir = filedialog.askdirectory()

clsSet = set()
files = glob.glob(inDir+"/*.xml")
for f in tqdm(files, desc = "Fetching Class Names Yo!"):
    tree = ET.parse(f)
    root = tree.getroot()

    for i in root.iter('name'):
        clsSet.add(i.text)

clsList = list(clsSet)
print(clsList)
clsNum = [x for x in range(0, len(clsList))]
clsDict = dict(zip(clsList, clsNum))
f = open("numClasses.txt", 'w')
f.write(str(clsDict))
f.close()