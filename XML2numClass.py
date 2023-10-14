import xml.etree.ElementTree as ET
from colorama import Fore, Style
from tkinter import filedialog
from tqdm import tqdm
import yaml
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
clsList.sort()
print(clsList)
clsNum = [x for x in range(0, len(clsList))]
clsDict = dict(zip(clsList, clsNum))
f = open("numClasses.txt", 'w')
f.write(str(clsDict))
f.close()

yamlDict = dict(
    train = "../train/images",
    val = "../valid/images",
    test = "../test/images",
    nc = len(clsDict.keys()),
    names = str(clsList)
)

f = open("data.yaml", 'w')
yaml.dump(yamlDict, f, default_flow_style=False)
f.close()