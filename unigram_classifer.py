# -*- coding: utf-8 -*-

import nltk
import re
from nltk import word_tokenize


class unigramClassifier:
    def __init__(self):
        self.unigrams_dictionary = {}

    def createDictionary(self,demographic):
        self.unigrams_dictionary = {}
        f = open('unigrams_dict_'+demographic+'.txt', 'r')
        for line in f:
            self.unigrams_dictionary[line.strip()] = 0

    def buildSet(self,line):
        line_split = line.split()
        if (line != '\n' and line_split != []):
            if (line_split[0] != 'RT'):
                line_split = word_tokenize(line.strip().decode("utf-8"))
                for word in line_split:
                    # Convert each n-gram to lowercase
                    word = word.lower()
                    # normalize links
                    if 'http' in word:
                        word = "###LINK###"
                    # normalize digits
                    word = re.sub('[0-9]+', "###DIGIT###", word)
                    # normalize @user
                    if word[0] == '@':
                        word = "###USER###"
                    if word in self.unigrams_dictionary:
                        # features[word] = features[word] + 1
                        self.unigrams_dictionary[word] = 1
