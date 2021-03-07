import spacy #External Library, requires download. 
import json
import math
import webbrowser
from tkinter import *
from collections import defaultdict
from tkinter import ttk as ttk
from bs4 import BeautifulSoup


indexData = defaultdict(dict)
N = 37497

count = 0
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
    queryWin.geometry("1600x1000")

    

    #Label for Title
    SEOname = Label(queryWin, text= "Geegle", fg = "red")
    
    SEOname.config(font=("Helvetica", 35))
    SEOname.place(relx = 0.5, rely = 0.05, anchor = 'center')
    #search box 
    searchBox = Entry(queryWin, width = 45)
    searchBox.place(relx = 0.5, rely = 0.09, anchor = 'center')
    
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
        #construct dictionary to store query term and their frequencies (tfdict) Wt,d=[1+ log("tft,d")] x log(N/dft)
        tfDict = defaultdict(int)
        for terms in query:
            tfDict[terms] += 1 
        #query doc frequency   
        dfDict = defaultdict(int)
        queryWeightDict = defaultdict(float)
 
        #document score dictionary, holding doc ids and their pre normalized scores. (Docterm weight * query term weight)
        docScore = defaultdict(float) 
        #document length dictionary, holding doc ids and their length. 
        docLength = defaultdict(float) 

        #get first letter of each search term to find the correct index 
        for each in set(query):
            alphabet = ord(each[0])
            if 47 < alphabet < 58:
                alphabetOrd = 0
            elif 96 < alphabet < 123:
                alphabetOrd = alphabet-96
            
            #check whether the word's first letter data is already stored, if not open file and create dictionary
            if  len(indexData[str(alphabetOrd)].items()) == 0:

            #open corresponding file names            
                fileName = str(alphabetOrd) + "indexEnd.txt"
                with open(fileName, "r", encoding="utf8") as f:
                    lines = f.readlines() 
                for line in lines:
                    #line.split(": ") is term : ids/weight (e.g. word: 0/10/1.23/tag)
                    termLine = line.split(": ") 
                    indexData[str(alphabetOrd)][termLine[0]] = termLine[1]

            #store posting list (e.g. 0/10/1.23/tag, 0/10/1.23/tag ) of each query term, and strip trailing spaces/endline characters    
            Ids = indexData[str(alphabetOrd)][each].rstrip()

            #trying to find the number of unique IDs (document freq of query terms)
            dfDict[each] = len(set(Ids.split()))
            #calculate and store query term weight into dictionary "Wt,d"=[1+ log(tft,d)] x log(N/dft)
            queryWeightDict[each] = round(((1 + math.log(tfDict[each])) * math.log(N/dfDict[each])),3)
            
            #list to hold docIds for lemma (Splits the posting list) 
            lemmaData = Ids.split()
            #lemmaData = ["0/10/weight/tag" ,]


            #calculate the score of the document and the document length
            #x = entire string of all info(weight and tag) for each ID 
            for x in lemmaData:
                #calculating cumulative pre normalized docScore for each possible docId
                #docScore = doc term weight * query term weight
                docScore[x] += float(x.split("/")[2]) *  queryWeightDict[each]
                #calculating length^2 for each possible docId
                docLength[x] += float(x.split("/")[2])**2

        #find query length ()
        queryLength = 0
        for ql in queryWeightDict:
            queryLength += queryWeightDict[ql]**2 
        
        queryLength = math.sqrt(queryLength)

        result = defaultdict(float)
        #for each possible docId, cosine score = prenormalizedDotProduct/querylength/documentlength 
        for scoreID in docScore:
            result[scoreID] = round(docScore[scoreID]/math.sqrt(docLength[scoreID])/queryLength, 3)
        
        #dictionary for html tag values
        tag ={"title": 0.00007, "strong": 0.00006, "h1": 0.00005, "h2": 0.00004, "h3": 0.00003, "p": 0.00002, "li": 0.00001  }
        #all the results' weight is added by their corresponding tag weight to distinguish
        #(misleading structure name
        # sortedResult = {k: v for k, v in sorted(result.items(), key = lambda item: item[1], reverse = True)})
        
        #dictionary holding docId and their score + html weight. 
        #resultDict[docID] = weight +html
        resultDict = {}        
        for IDinfo, dScore in result.items():
            
            docID = IDinfo.split("/")[0] + "/" + IDinfo.split("/")[1]
            
            tags = IDinfo.split("/")[3].split(",")
            
            for each in tags:
                dScore += tag[each]
            resultDict[docID] = dScore
        
        count = len(resultDict)
        print("link count: " + str(count))
        resultList = [k for k, v in sorted(resultDict.items(), key = lambda item: item[1], reverse = True)] [:20]
        #resultList = [k for k, v in sorted(resultDict.items(), key = lambda item: item[1], reverse = True)]
        # print(sorted(resultDict.items(), key = lambda item: item[1], reverse = True)[:20])
        # result = resultList
                    
        
        #result frame
        #construct html file and open in chrome
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
            return 
            
        #return links from objID using json file
        jsonFile = r"C:\Users\james\UC Irvine\cs121 information retrieval\Assignment Three part 1\webpages\WEBPAGES_RAW\bookkeeping.json"
        basePath = r"C:\Users\james\UC Irvine\cs121 information retrieval\Assignment Three part 1\webpages\WEBPAGES_RAW"
        with open(jsonFile, 'r') as f:
            json_object = json.load(f)
            #print first 20 results
            resultCount = 0

            for widgets in resultDisplay.winfo_children():
                widgets.destroy()

            resultBox= ttk.Labelframe(resultDisplay, text="Results")
            resultBox.place(relx = 0.5, rely = 0.5, anchor = 'center')
            resultBox.pack()

            for keys in resultList:
                #print(keys)
                resultCount += 1
               
                link = json_object[keys]
                #displayResultLine = Button(resultDisplay, text =  link, fg ="blue", command = lambda: callback(self.cget("text")) )
                #construct file path and pass into callback
                


                split = keys.split("/")
                dataPath= basePath + "\\" + split[0] + "\\" + split[1]
                htmlData = open(dataPath, encoding = "UTF-8")
                soup = BeautifulSoup(htmlData, "lxml")
                
                #TO DO: PARSE THE TITLE
               
                description = soup.get_text().replace("\n", " ")
                if len(description) > 105:
                    description = description[0:105]
                
                description = " ".join(description.split())
                
                print("description: " + description)
               
                container = Label(resultBox, width = 200, height = 100)
                container.pack()
                title = ""
                if len(link) > 45:
                    title = link[:45] + "..."
                else:
                    title = link
                displayResultLine= Button(container, text= str(resultCount)+". " +title , fg = "blue", borderwidth= 0, command=lambda url = dataPath: callback(url))
                displayResultLine.config(font = ('Calibri', 9))
                displayResultLine.pack()
                descriptionLabel = Label(container, text = description + "1")
                descriptionLabel.config(font = ('Calibri', 7))
                descriptionLabel.pack()

            
                print(str(resultCount) + ". " + link)
            if len(resultList) == 0:
                notFound = Label(resultDisplay, text = "Oops, results not found!")
                notFound.pack()

        return 
    
    searchButton = Button(queryWin, text = "Search", command = lambda: getQuery())
    searchButton.place(relx = 0.5, rely = 0.12, anchor = 'center') 

    resultDisplay = ttk.Panedwindow(queryWin, orient= VERTICAL)
    resultDisplay.place(relx = 0.5, rely = 0.56, anchor = 'center')
    
    queryWin.mainloop()
