import PullIdGenTweetText
import makewordcloud
from stacked_classifier import StackedClassifier


def tweets(entered):
    name = PullIdGenTweetText.getTweeterInfo(entered)
    makewordcloud.makecloud(entered)
    stacked = StackedClassifier(entered,name)
    gender,age = stacked.get_labels()
    wordcloud = 'static/' + entered + '_cloud.png'
    return age,gender,wordcloud,name

def classified(handle):
    age, gender, wordcloud,name = tweets(handle)
    profile_pic = 'static/' + handle + '.png'
    py_obj = [handle, age, gender.lower(), wordcloud, name, profile_pic]
    return py_obj
