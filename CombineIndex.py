from collections import defaultdict
import codecs

for i in range(27):
    #dictionary to hold first doc
    first = defaultdict(str)
    fileName = str(i) + "FortyToFifty.txt"
    with open(fileName, "r", encoding = "utf8") as f:
    #dictionary holding all the lemms in the text file and their doc ids     
        lines = f.readlines() 
        for line in lines:
            termLine = line.split(": ") 
            first[termLine[0]] = termLine[1].rstrip()
    
    #dictionary to hold the second doc
    second = defaultdict(str)
    fileName = str(i) + "FiftyToFiftyNine.txt"
    with open(fileName, "r", encoding = "utf8") as f:
    #dictionary holding all the lemms in the text file and their doc ids     
        lines = f.readlines() 
        for line in lines:
            termLine = line.split(": ") 
            second[termLine[0]] = termLine[1].rstrip()
    
    
    for key in second: 
        if key in first:
            first[key] = first[key] + second[key]
        else:
            first[key] = second[key]
    
    
    #print dictionary to file
    fileName = str(i) + "OneToSixty.txt" 
    with codecs.open(fileName, "w", 'UTF-8') as file:        
        for lem in first: #for each lemma in dictionary
            #term frequency
            
            output = lem + ": " + first[lem]
            file.write(output + "\n")


