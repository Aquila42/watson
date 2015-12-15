import json
from flask import jsonify
from getTweets import tweets
import random


def classified(handle):
    print "in classify"
    age, gender, wordcloud = tweets(handle)
    print age
    print gender
    print wordcloud
    py_obj = [age, gender, wordcloud]
    return py_obj
