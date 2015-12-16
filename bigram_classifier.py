# -*- coding: utf-8 -*-

import re
from nltk import word_tokenize


class bigramClassifier:
    def __init__(self):
        self.bigrams_dictionary = {}

    def createDictionary(self,demographic):
        self.bigrams_dictionary = {}
        f = open('bigrams_dict_'+demographic+'.txt', 'r')
        for line in f:
            self.bigrams_dictionary[line.strip()] = 0

    def buildSet(self, line):
        line_split = line.split()
        if (line != '\n' and line_split != []):
            if (line_split[0] != 'RT'):
                line_split = word_tokenize(line.strip().decode("utf-8"))
                for i in range(0, len(line_split)):
                    # Convert each n-gram to lowercase
                    if (i + 1 <= len(line_split) - 1):
                        word = line_split[i].lower()
                        next_word = line_split[i + 1].lower()
                        # normalize links
                        if 'http' in word:
                            word = "###LINK###"
                        if 'http' in next_word:
                            next_word = "###LINK###"
                        # normalize digits
                        word = re.sub('[0-9]+', "###DIGIT###", word)
                        next_word = re.sub('[0-9]+', "###DIGIT###", next_word)
                        # normalize @user
                        if word[0] == '@':
                            word = "###USER###"
                        if next_word[0] == '@':
                            next_word = "###USER###"
                        bigram = word + " " + next_word
                        if bigram in self.bigrams_dictionary:
                            self.bigrams_dictionary[bigram] = 1
