import PullIdGenTweetText
import makewordcloud
import sys
import random

def tweets(entered):
	name=PullIdGenTweetText.getTweeterInfo(entered)

	filename=makewordcloud.makecloud(entered)
	gender_num = random.randrange(0,2)
	if gender_num == 0:
		gender = 'female'
	else:
		gender = 'male'
	#age classifier:
	age = str(random.randrange(16,100)) #turn age into string if needed
	wordcloud = 'static/'+entered+'_cloud.png'
	print age
	print gender
	print wordcloud
	return age,gender,wordcloud