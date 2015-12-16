from getTweets import tweets


def classified(handle):
    print("In classify")
    age, gender, wordcloud,name = tweets(handle)
    profile_pic = 'static/' + handle + '.png'
    py_obj = [handle, age, gender.lower(), wordcloud, name, profile_pic]
    print("Returning py_obj")
    return py_obj
