import PullIdGenTweetText
import makewordcloud
import sys
import random
from stacked.stacked_classifier import StackedClassifier


def tweets(entered):
    name = PullIdGenTweetText.getTweeterInfo(entered)
    filename = makewordcloud.makecloud(entered)
    stacked = StackedClassifier(entered,name)
    gender,age = stacked.get_labels()
    wordcloud = 'static/' + entered + '_cloud.png'
    print age
    print gender
    print wordcloud
    # return age, gender, wordcloud
    return age,gender,wordcloud
