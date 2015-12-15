import json
from flask import jsonify
from getTweets import tweets
import random


def classified(handle):
    age, gender, wordcloud,name = tweets(handle)
    py_obj = [handle, age, gender.lower(), wordcloud, name]
    return py_obj
