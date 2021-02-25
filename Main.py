#change log: 
# Line 23->added to lower to account for capitalized searches
# Line 99: casted to list since .key() returns a view not list and cannot be subscripted. 


import spacy #External Library, requires download. 
import json
from collections import defaultdict
 
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


if __name__ == "__main__":

    queries = input("What are you searching for: ")
    queries = queries.lower()
    #print(queries)
    #if we want to do ranking, make these sets into list and apply the following lines:
    #allID= [(set),(set),(set)]
    # 'software': ('0/101','0/100')
    # revisionsbacklink': ['0/101', '0/100 ' 98']
    # startsoftwarearem': ['0/101','0/99' 98]}
    # allID(101*3 100X2 99X1 98X2)
    # 101
    # 100
    # 99
    # 98
    # union = [sum of allID]
    # for each in union:
    #     if in allid[1] +1 
    
    #lemmatize query input 
    sp = spacy.load('en_core_web_sm')
    lemmas = sp(queries)
    lemmas = [x for x in lemmas if str(x) not in stopWords]
    
    query = [] # to hold lemmatized, alphanumeric query inputs
    
    #remove non alphanumeric query terms 
    for token in lemmas:        
        lemmaStr = str (token.lemma_)
        if all(x.isalnum() for x in lemmaStr):
            query.append(lemmaStr)

    print(query)
    #return the index from the first letter of the search term so we know which file to look. 
    allID = defaultdict(int)
    for each in query:
        alphabet = ord(each[0])
        if 47 < alphabet < 58:
            alphabetOrd = 0
        elif 96 < alphabet < 123:
            alphabetOrd = alphabet-96

        #open corresponding file names            
        fileName = str(alphabetOrd) + ".txt"
        #print(fileName)
        with open(fileName, "r", encoding="utf8") as f:
            wordInTextFile = {}
            lines = f.readlines() 
            for line in lines:
                wordAndID  = line.split(": ") #list ["term1", "list of docID term2" 
                wordInTextFile[wordAndID[0]] = set(wordAndID[1].split())
            
        
        if each in wordInTextFile:
            for docId in wordInTextFile[each]:
                allID[docId] += 1
        
        sortedValues = sorted(allID.values(), reverse = True) # Sort the values
        sortedID = {}

        for i in sortedValues:
            for j in allID.keys():
                if allID[j] == i:
                    sortedID[j] = allID[j]
        



    #{term: [all ID]}
    # => {term: {IDS: tf-iDf(weight)}
        
    # query: normalize and dot product with query vector.           
    #print(allID)
    #print(sortedID)
    print("number of links: ", len(sortedID.keys()))
    #return links from objID using json file
    jsonFile = r"C:\Users\james\UC Irvine\cs121 information retrieval\Assignment Three part 1\webpages\WEBPAGES_RAW\bookkeeping.json"
    with open(jsonFile, 'r') as f:
        json_object = json.load(f)
        #print first 20 results
        resultCount = 0
        
        if len(sortedID) > 20:
            top_result = list(sortedID.keys())[:20]
        else:
            top_result = sortedID.keys()

        for keys in top_result:
            resultCount+= 1
            
            print(str(resultCount), json_object[keys])
            


    




    
    
    
        
        
