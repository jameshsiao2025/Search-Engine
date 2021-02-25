#0/101
import os
import json
import codecs
import re
from bs4 import BeautifulSoup
from collections import defaultdict
from defaultlist import defaultlist

basePath = r"C:\Users\james\UC Irvine\cs121 information retrieval\Assignment Three part 1\webpages\WEBPAGES_RAW"
dataPath = basePath + "\\" + "0" + "\\" + "2"
htmlData = open(dataPath, encoding = "UTF-8") 


soup = BeautifulSoup(htmlData, "lxml")
ptext = soup.find_all("p")
ptext = ptext.text.strip()
print(ptext)
# for heading in ptext:
#     print(heading.name + " : " + heading.text.strip())
#h1 (0.20): alumni [1.2] 
#htext = soup.find_all(['h'])
#print(ptext)
#print(htext)