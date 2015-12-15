import PullIdGenTweetText
import makewordcloud
import sys
import random
from stacked_classifier import StackedClassifier


def tweets(entered):
	print "in get tweets"
	name = PullIdGenTweetText.getTweeterInfo(entered)
	print name
	filename = makewordcloud.makecloud(entered)
	print filename
	stacked = StackedClassifier(entered,name)
	gender,age=stacked.get_labels()
	wordcloud='static/' + entered + '_cloud.png'
	print age
	print gender
	print wordcloud
	return age,gender,wordcloud