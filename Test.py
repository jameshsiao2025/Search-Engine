# from bs4 import BeautifulSoup
# import spacy

# basePath = r"C:\Users\james\UC Irvine\cs121 information retrieval\Assignment Three part 1\webpages\WEBPAGES_RAW"

counter = 0
total = 0
while counter < 27:
    fileName = str(counter) + ".txt"
    with open(fileName, "r", encoding = "utf8") as f:
        lines = f.readlines() 
        total += len(lines)
    counter += 1

print("word count: ", total)