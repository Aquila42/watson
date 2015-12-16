import PullIdGenTweetText
import makewordcloud
from stacked_classifier import StackedClassifier


def tweets(entered):
    name = PullIdGenTweetText.getTweeterInfo(entered)
    makewordcloud.makecloud(entered)
    stacked = StackedClassifier(entered,name)
    print("Getting age and gender")
    gender,age = stacked.get_labels()
    wordcloud = 'static/' + entered + '_cloud.png'
    print age
    print gender
    print wordcloud
    # return age, gender, wordcloud
    return age,gender,wordcloud,name
