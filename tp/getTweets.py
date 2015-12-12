import PullIdGenTweetText
import makewordcloud
import sys

def tweets(entered):
	name=PullIdGenTweetText.getTweeterInfo(entered)

	filename=makewordcloud.makecloud(entered)

	age="25+"
	gender="Female"
	print str(entered+"\t"+name+"\t"+age+"\t"+gender+"\t"+filename)