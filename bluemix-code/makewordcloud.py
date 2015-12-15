from wordcloud import WordCloud
from nltk.corpus import stopwords
import matplotlib.pyplot as plt
import json
import sys


def makecloud(name):
    cnt = 0
    # file=open('age_over54_train/KABarron.txt')
    file = open(name + ".txt")
    demo_text = ""
    print "In wordcloud"
    stop = stopwords.words('english')
    for line in file:
        if cnt < 2:
            cnt += 1
        elif cnt < 52:
            line = line.strip().replace("'", "").replace('"', '')
            if str(line).startswith("RT"):
                continue
            else:
                newline = [i for i in line.split() if i not in stop]
                finsent = ""
                for word in newline:
                    if "@" in word or "https" in word or ".co" in word or "http" in word:
                        continue
                    else:
                        finsent += word + " "

                demo_text += finsent + " "
            cnt += 1
        else:
            break
    filename = 'static/'+ name + '_cloud.png'
    print "send to maker"
    wordcloud = WordCloud(max_font_size=500,width=900,height=600,background_color='white',prefer_horizontal=0.5,font_path="a song for jennifer.ttf").generate(demo_text)
    print "send to file"
    wordcloud.to_file(filename)
    print "out wordcloud"
    return str(name + '_cloud.png')