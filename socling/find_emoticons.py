import glob
from nltk import word_tokenize
import re

def check_emoticon(word):
    emoticons = [":)","(:",":p",":d","d:",":(","):"]
    if token.lower() in emoticons:
        return True
    if token.isalpha() or token.find("http") > -1:
        return False
    if re.match(".+:.+",token):
        return True


emoticons = {}
for filename in glob.glob('../data/*.txt'):
    f = open(filename,"r")
    for line in f:
        tokens = line.strip().decode('utf-8').split()
        for token in tokens:
            if check_emoticon(token):
                if token not in emoticons:
                     emoticons[token] = 1
                else:
                    emoticons[token] += 1
print emoticons