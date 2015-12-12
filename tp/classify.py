import json
from flask import jsonify
from getTweets import tweets
import random


def classified(handle):
	tweets(handle)
	#gender classifier:
	gender_num = random.randrange(0,2)
	if gender_num == 0:
		gender = 'female'
	else:
		gender = 'male'
	#age classifier:
	age = str(random.randrange(16,100)) #turn age into string if needed
	#interests (an array):
#	interests = ['movies','theater']
	wordcloud = 'static/'+handle+'_cloud.png'
	py_obj = [age, gender, wordcloud] #example ['18', female, ['movies','theater']
#	json_string = {}
	return py_obj

	'''
	json_string = json.dumps(py_obj)
	return json_string
	#use python dic instead of json
	'''

