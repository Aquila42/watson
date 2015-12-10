#import json
#from flask import jsonify
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
	age = str(random.randrange(16,100)) 
	#interests (an array):
	interests = ['movies','theater']
	py_obj = [age, gender, interests] #example ['18', female, ['movies','theater']
	return py_obj



