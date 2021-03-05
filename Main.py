#change log: 
# Line 23->added to lower to account for capitalized searches
# Line 99: casted to list since .key() returns a view not list and cannot be subscripted. 


import spacy #External Library, requires download. 
import json
import math
import webbrowser
from tkinter import *
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
    
    #GUI Set up
    queryWin = Tk()
    queryWin.title("Let's Grab Boba Team 15_SEO")
    queryWin.geometry("2500x1000")

    #Label for Title
    SEOname = Label(queryWin, text= "Geegle", fg = "red")
    
    SEOname.config(font=("Helvetica", 50))
    SEOname.place(relx = 0.5, rely = 0.3, anchor = 'center')
    #search box 
    searchBox = Entry(queryWin, width = 45)
    searchBox.place(relx = 0.5, rely = 0.37, anchor = 'center')
    
    result = {}
    webbrowser.register('chrome', None, webbrowser.BackgroundBrowser("C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"))

    def getQuery():
        
        
        queries =  searchBox.get().lower()
        sp = spacy.load('en_core_web_sm')
        lemmas = sp(queries)
        lemmas = [x for x in lemmas if str(x) not in stopWords]
        
        query = [] # to hold lemmatized, alphanumeric query inputs
        
        #remove non alphanumeric query terms 
        for token in lemmas:        
            lemmaStr = str (token.lemma_)
            if all(x.isalnum() for x in lemmaStr):
                query.append(lemmaStr)

        #calculate weight for query terms 
        print("you searched for: ", query)
        #query term frequency
        tfDict = defaultdict(int)
        for terms in query:
            tfDict[terms] += 1 
        #query doc frequency   
        dfDict = defaultdict(int)
        queryWeightDict = defaultdict(float)

        
        #return the index from the first letter of the search term so we know which file to look. 
        allID = defaultdict(int)
        
        

        

        #document score dictionary, holding doc ids and their scores. 
        docScore = defaultdict(float)   
        docLength = defaultdict(float)          
        for each in set(query):
            alphabet = ord(each[0])
            if 47 < alphabet < 58:
                alphabetOrd = 0
            elif 96 < alphabet < 123:
                alphabetOrd = alphabet-96

            #open corresponding file names            
            fileName = str(alphabetOrd) + "indexEnd.txt"
            #print(fileName)
            with open(fileName, "r", encoding="utf8") as f:
                #dictionary holding all the lemms in the text file and their doc ids 
                
                lines = f.readlines() 
                for line in lines:
                    termLine = line.split(": ") 
                    if termLine[0] == each:
                        #line.split(": ") is term : ids/weight (e.g. word: 0/10/1.23/tag)
                        
                        #trying to find the number of unique IDs (docu freq)
                        dfDict[each] = len(set(termLine[1].split()))
                        queryWeightDict[each] = round(((1 + math.log(tfDict[each])) * dfDict[each]),3)
                        
                        #list to hold docIds for lemma
                        #print(line)
                        lemmaData = termLine[1].split()
                        for x in lemmaData:
                            #print(x.split("/")[2])
                            docScore[x] += float(x.split("/")[2]) *  queryWeightDict[each]
                            docLength[x] += float(x.split("/")[2])**2
        

        #find query length
        queryLength = 0
        for ql in queryWeightDict:
            queryLength += queryWeightDict[ql]**2 
        
        queryLength = math.sqrt(queryLength)

        result = defaultdict(float)
        for dScore in docScore:
            result[dScore] = round(docScore[dScore]/docLength[dScore]/queryLength, 3)
        
        
        
        
        #<title> <strong><h1> <h2> <h3><p><li>
        tag ={"title": 0.00007, "strong": 0.00006, "h1": 0.00005, "h2": 0.00004, "h3": 0.00003, "p": 0.00002, "li": 0.00001  }
        #all the results' weight is added by their corresponding tag weight to distinguish
        #misleading structure name
        sortedResult = {k: v for k, v in sorted(result.items(), key = lambda item: item[1], reverse = True)}
        
        # [:20]                   
        #{0/10/0.2/tag: weight}
        resultDict = {}
        
        for k, dScore in sortedResult.items():
            
            docID = k.split("/")[0] + "/" + k.split("/")[1]
            
            tags = k.split("/")[3].split(",")
            #print(tags)
            for each in tags:
                dScore += tag[each]
            resultDict[docID] = dScore
        #print("result: ")
        #print(resultDict)

        resultList = [k for k, v in sorted(resultDict.items(), key = lambda item: item[1], reverse = True)] [:20]
        #print(resultList)
        result =resultList
                    
        
        #result frame

       

        def callback(link):

            #text data
            data = ""
            with open(link, 'r') as f:
                data = f.read()
            newPath = link + ".html"
            with open(newPath, 'w') as f1:
                f1.write(data)


            webbrowser.get('chrome').open(newPath, new=2)
            #webbrowser.open(link, new=2)
            
        #return links from objID using json file
        jsonFile = r"C:\Users\james\UC Irvine\cs121 information retrieval\Assignment Three part 1\webpages\WEBPAGES_RAW\bookkeeping.json"
        basePath = r"C:\Users\james\UC Irvine\cs121 information retrieval\Assignment Three part 1\webpages\WEBPAGES_RAW"
        with open(jsonFile, 'r') as f:
            json_object = json.load(f)
            #print first 20 results
            resultCount = 0

            for widgets in resultDisplay.winfo_children():
                widgets.destroy()


            for keys in resultList:
                #print(keys)
                resultCount += 1
               
                
                link = json_object[keys]
                #displayResultLine = Button(resultDisplay, text =  link, fg ="blue", command = lambda: callback(self.cget("text")) )
                #construct file path and pass into callback
                split = keys.split("/")
                dataPath= basePath + "\\" + split[0] + "\\" + split[1]
                print(dataPath)
                displayResultLine = Button(resultDisplay, text = str(resultCount) + ". " + link, fg ="blue", command=lambda url = dataPath: callback(url))
                
               
                displayResultLine.pack()
                
               
    

                print(str(resultCount) + link)
            if len(resultList) == 0:
                notFound = Label(resultDisplay, text = "Oops, results not found!")
                notFound.pack()

        return 
    
    searchButton = Button(queryWin, text = "Search", command = lambda: getQuery())
    searchButton.place(relx = 0.5, rely = 0.40, anchor = 'center') 

    resultDisplay = Frame(queryWin)
    resultDisplay.place(relx = 0.5, rely = 0.7, anchor = 'center')
    


    queryWin.mainloop()


#{0/10/tag: 1.25 +7, 0/20: 1.25 +4}
#TO DO LIST :
#1. Tags (Sat) DONE
#2. Make txt file smaller ()
#3. GUI (Sun-Mon) DOING 
#4. redivide back the log for doc freq after the index is done :) (next week)
#5. TA Meeting Schedule DONE


            


    




    
    
    
        
        
