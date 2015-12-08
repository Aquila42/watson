import glob
from nltk import word_tokenize,bigrams

f = open("feature_files/possessive_bigrams.txt","w")
for feature in features_list:
    f.write(feature+"\n")
f.close()