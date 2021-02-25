from collections import Counter
from collections import defaultdict
import math
import codecs
#N = total number of documents in corpus;
N = 37497

# term frequency per doc (tft,d)
# go through each term, and create a dictionary that holds the frequency of each doc id for the term.
#open corresponding file names  
#           
#fileName = str(alphabetOrd) + ".txt"


#print(fileName)
for x in range(27):
    ranking = defaultdict(str)
    
    fileName = str(x) + '.txt'    
    with open(fileName, "r", encoding = "utf8") as f:
        wordInTextFile = {}
        lines = f.readlines()
        termFrequencyCounter = {} 
        documentFrequency = defaultdict(int)
        for line in lines:
            wordAndID  = line.split(": ") #list ["term1", "list of docID term2" 
            #[0/1 0/2 0/2 0/3]
            #Counter({0/1:, 0/2:2, 0/3})
            # term frequency per doc (tft,d)
            #{term: [{doc: freq, doc: freq, doc: freq,dft]}
            #term: dft
            #A counter of how many times/how frequent is this term in each DOC
            freq = Counter(wordAndID[1].split())
            #print(wordAndID[0], freq)
            termFrequencyCounter[wordAndID[0]] = freq
            #print(termFrequencyCounter[wordAndID[0]])
            documentFrequency[wordAndID[0]] = len(freq)
            #print(len(termFrequencyCounter))
            #print(documentFrequency)

        for terms in termFrequencyCounter:
            for docIds in termFrequencyCounter[terms]:
                tf = termFrequencyCounter[terms][docIds]
                df = documentFrequency[terms]
                tflog = math.log(termFrequencyCounter[terms][docIds])
                dflog=  (math.log(N/documentFrequency[terms]))
                docWeight = round((1 + tflog)* dflog, 3)
                #print(terms, docIds, tf, df)
                ranking[terms] += " " + str(docIds) + "/" + str(docWeight)
        
    #print(ranking)
               
    fileName = str(x) + "_ranking.txt" 
    with codecs.open(fileName, "w", 'UTF-8') as file:        
        for items in ranking: 
            file.write(items + ": " + ranking[items] + "\n")


           
            

#Dictionary Structure
#{term : docid/weight:STRING)}}}     apple: 0/0/23.5 2/34/5.2 3/12/2.4 
    
#print to doc 
# if each in wordInTextFile:
#     for docId in wordInTextFile[each]:
#         allID[docId] += 1
# doc frequency per term (dft) 

# weighting 