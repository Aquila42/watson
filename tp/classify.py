import json
from flask import jsonify
from getTweets import tweets
import random


def classified(handle):
	age,gender,wordcloud=tweets(handle)
	print age
	print gender
	print wordcloud
	py_obj = [age, gender, wordcloud] #example ['18', female, ['movies','theater']
#	json_string = {}
	return py_obj

	'''
	json_string = json.dumps(py_obj)
	return json_string
	#use python dic instead of json
	'''

