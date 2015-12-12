# -*- coding: utf-8 -*-

import nltk
import re
from nltk import word_tokenize

class unigramClassifier:

	def __init__(self):
		self.unigrams_dictionary = createDictionary()
		# buildSet()		
		
	def createDictionary(self):	
		f = open('unigrams_dict.txt','r'):
		f_line = f.readline()
		while f_line:
			f_line = f_line.strip()
			self.unigrams_dictionary[f_line] = 0
			f_line = f.readline()		

	def buildSet(self):		
		line_split = line.split()
		if (line != '\n' and line_split != []):
			if (line_split[0] != 'RT'):
				line_split = word_tokenize(line.strip().decode("utf-8"))
				# line_split = gettokens.tokenize(line.strip())
				for word in line_split:
					# Convert each n-gram to lowercase
					word = word.lower()
					# normalize links			
					if 'http' in word:
						word = "###LINK###"
					# normalize digits		
					word = re.sub('[0-9]+',"###DIGIT###",word)
					# normalize @user 
					if word[0] == '@':
						word = "###USER###"
					if word in self.unigrams_dictionary:
						# features[word] = features[word] + 1						
						self.unigrams_dictionary[word] = 1
