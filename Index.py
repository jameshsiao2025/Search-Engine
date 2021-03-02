import os
import json
import codecs
import math
import re
from bs4 import BeautifulSoup
from collections import defaultdict
from defaultlist import defaultlist

import spacy #External Library, requires download. 
N = 37497

#Data stucture [{a_vocab : index +'-tag', }, {b_dict}, ]
indexArray = defaultlist(dict)

inverseIndex = {}
stopWords = ["a","about","above","after","again","against","all","am","an","and","any","are","aren't","as","at","be","because",
"been","before","being","below","between","both","but","by","can't","cannot","could","couldn't","did",
"didn't","do","does","doesn't","doing","don't","down","during","each","few","for","from","further","had","hadn't",
"has","hasn't","have","haven't","having","he","he'd","he'll","he's","her","here","here's","hers","herself","him","himself",
"his","how","how's","i","i'd","i'll","i'm","i've","if","in","into","is","isn't","it","it's","its","itself","let's","me","more","most","mustn't",
"my","myself","no","nor","not","of","off","on","once","only","or","other","ought","our","ours",
"ourselves","out","over","own","same","shan't","she","she'd","she'll","she's","should","shouldn't","so","some","such",
"than","that","that's","the","their","theirs","them","themselves","then","there","there's","these","they","they'd","they'll",
"they're","they've","this","those","through","to","too","under","until","up","very","was","wasn't","we","we'd","we'll","we're",
"we've","were","weren't","what","what's","when","when's","where","where's","which","while","who","who's","whom","why",
"why's","with","won't","would","wouldn't","you","you'd","you'll","you're","you've","your","yours","yourself","yourselves"]

punctuation = ["?",":", "!", ".", ",", ";", "[", "]", "&", "$", "-"]

def listToString(s):      
    # initialize an empty string 
    str1 = ""      
    # traverse in the string   
    for ele in s:  
        str1 += ele + " "    
    # return string   
    return str1

#also change these two paths 
#file = r"C:\Users\james\UC Irvine\cs121 information retrieval\Assignment Three part 1\webpages\WEBPAGES_RAW\bookkeeping2.json"
file = r"C:\Users\james\UC Irvine\cs121 information retrieval\Assignment Three part 1\webpages\WEBPAGES_RAW\17001.json"
basePath = r"C:\Users\james\UC Irvine\cs121 information retrieval\Assignment Three part 1\webpages\WEBPAGES_RAW"
with open(file, 'r') as f:

    json_object = json.load(f)
    #index = 0
    for path in json_object : 
        
        # if(index == 5):
        #     break 
        # index +=1
        objId = path
        split = objId.split("/")
        dataPath= basePath + "\\" + split[0] + "\\" + split[1]

        htmlData = open(dataPath, encoding = "UTF-8")
        soup = BeautifulSoup(htmlData, "lxml")
        #text = soup.find_all()
        tags = ['p', 'title','h1','h2','h3','strong','li']
        #loop over the tags and find text in each tag, split them into phrase
        for tag in tags:
            textSet = soup.find_all(tag)
            for heading in textSet:
                text = heading.text.strip()

                #splitting up into section when they are too big.       
                splitText = text.split()
                textList = []
                limit = 50000
                if len(splitText) > 50000:
                    while len(splitText) > 50000:
                        textList.append(splitText[0 : 50000])
                        splitText = splitText[50001 : len(splitText)-1]
                else:
                    textList.append(splitText)

                lemmaList = []
                
                for textSegments in textList:
                    text = " ".join(textSegments)
                    #tokenize the text for the tag
                    sp = spacy.load('en_core_web_sm')
                    sp.max_length = 3000000
                    tokenizedText = sp(text)
                    #token list
                    tokenizedText = [x for x in tokenizedText if str(x) not in stopWords]
                    for token in tokenizedText:
                        
                        lemmaStr = str (token.lemma_)

                        if all(x.isalnum() for x in lemmaStr):
                            lemmaList.append(lemmaStr)

                    for lemma in lemmaList:
                        this = (objId, tag)
                        alphabetOrder = ord(lemma[0])
                        
                        if 47 < alphabetOrder < 58: #Numbers 48 = 0, 57 = 9
                            #this = (objId, tag)
                            if lemma not in indexArray[0].keys():
                                indexArray[0][lemma] = []
                                
                                indexArray[0][lemma].append(this)
                            else:
                                #this = (objId, tag)
                                indexArray[0][lemma].append(this)
                        elif 96 < alphabetOrder < 123:
                            if lemma not in indexArray[alphabetOrder-96].keys():
                                indexArray[alphabetOrder-96][lemma] = []
                                indexArray[alphabetOrder-96][lemma].append(this)
                            else:
                                indexArray[alphabetOrder-96][lemma].append(this)
        
        print ("Last File Processed: " + objId)
#print(indexArray)

# for key in inverseIndex:
#     print (key + ":", end =" ")
#     print(inverseIndex[key])

#print statements for index.txt
nameCounter = 0
for alphabetDict in indexArray: #for each dictionary in list
    fileName = str(nameCounter) + "ThirtyToForty.txt" 
    with codecs.open(fileName, "w", 'UTF-8') as file:        
        for lem in alphabetDict: #for each lemma in dictionary
            #term frequency
            
            output = lem + ": "
            
            idList = defaultdict(list)
            #{id: [p,t,h.p]}
            
            for docIDs in alphabetDict[lem]:
                
                idList[docIDs[0]].append(docIDs[1])
            
             #incase
            
            #docFrequency = len(set(idList))
            
            for ids in idList:
                tfreq = len(idList[ids])
                tflog = math.log(tfreq)
                # print(tfreq)
                # print(tflog)
                #dflog = math.log(N/docFrequency)
                #print(dflog)
                docWeight = round((1 + tflog), 3)
                output += " "+ ids + "/" + str(docWeight) + "/" + ",".join(idList[ids]) 
                 
            #for each docID in counter, we will calculate the weight and store info
            #then we have to go back and match the doc Ids with the tags, and print into text file. 
            
            #doc frequency 
            file.write(output + "\n")
    nameCounter += 1 

