from SocioLinguistic import SocioLinguistic
from sklearn import linear_model, metrics
#from nltk import word_tokenize
from tweetokenize import Tokenizer
import get_age_or_gender
import glob
import time
import numpy as np
import re

class Classifier:
    def __init__(self):
        self.socling = SocioLinguistic()
        self.features_list = []
        self.features = {}
        self.labels = {}
        self.gettokens = Tokenizer()

    def label_file_to_dict(self,filename):
        dict_x = {}
        for line in open(filename,"r"):
            # print line
            temp = line.split("||")
            name = temp[0].strip()
            label = temp[1].strip()
            dict_x[name] = label
        return dict_x

    def create_features_list(self):
        self.socling.sent = "Some sentence"
        self.features_list.extend(self.socling.emoticons())
        self.features_list.extend(self.socling.excitement())
        self.features_list.extend(self.socling.single_exclam())
        self.features_list.extend(self.socling.ellipses())
        self.features_list.extend(self.socling.create_possessive_bigrams())
        self.features_list.extend(self.socling.pumping())
        self.features_list.extend(self.socling.self())
        self.features_list.extend(self.socling.laugh())
        self.features_list.extend(self.socling.shout())
        self.features_list.extend(self.socling.exasperation())
        self.features_list.extend(self.socling.agreement())
        self.features_list.extend(self.socling.honorifics())
        self.features_list.extend(self.socling.affection())
        self.features_list.extend(["RETWEETS"])
        f = open("feature_files/feature_names","w")
        for feature in self.features_list:
            try:
                f.write(feature+"\n")
            except:
                continue
        f.close()


    def get_features(self,line):
        self.socling.sent = line
        self.socling.sent_list = self.gettokens.tokenize(line.upper())
        start = time.time()
        self.socling.emoticons()
        end = time.time()
        #print("Emoticons:",end-start)
        start = time.time()
        self.socling.excitement()
        end = time.time()
        #print("Excitement:",end-start)
        self.socling.single_exclam()
        self.socling.ellipses()
        self.socling.possessive_bigrams(self.features_list)
        self.socling.pumping()
        self.socling.self()
        self.socling.laugh()
        self.socling.shout()
        self.socling.exasperation()
        self.socling.agreement()
        self.socling.honorifics()
        self.socling.affection()

    def reset_dictionary(self):
        for feature in self.features_list:
            self.features[feature] = 0

    def file_to_list(self,f):
        tweets = []
        retweets = 0
        for line in f:
            if line.strip() == "":
                continue
            elif line[:1] == "RT":
                retweets += 1
            else:
                line = re.sub('https?:\/\/.*[\r\n]*', '', line)
                #print(line)
                tweets.append(line.strip())
        f.close()
        return tweets,retweets

    def initialize(self):
        self.labels = self.label_file_to_dict("../all_labels_"+demographic+".txt")
        self.features_list = set(self.socling.file_to_list("feature_files/feature_names"))

    def features_from_file(self,f):
        features = []
        labels = []
        for line in f:
            temp = line.strip().split("||")
            feature = temp[0].strip().split("\t")
            label = temp[1].strip()
            features.append(np.array(feature).astype(float))
            labels.append(label)
        return features,labels

    def logistic_regression(self,demographic):
        train = open("svm/"+demographic+"_train","r")
        test = open("svm/"+demographic+"_test","r")
        train_features,train_labels = self.features_from_file(train)
        test_features,test_labels = self.features_from_file(test)
        clf = linear_model.LogisticRegression()
        clf.fit(train_features, train_labels)
        predicted = clf.predict(test_features)
        print("Logistic Regression:",metrics.accuracy_score(predicted,test_labels))

    def features_svm(self,file_type,demographic):
        output = open("svm/"+demographic+"_"+file_type,"w")
        for filename in glob.glob("../"+demographic+"_"+file_type+"/*.txt"):
            #filename = "../gend_train/215__chris.txt"
            print(filename)
            for feature in self.features_list:
                self.socling.features_dict[feature] = 0
            self.reset_dictionary()
            self.socling.features_dict = self.features
            f = open(filename,"r")
            user_name = f.readline().strip()
            try:
                label = self.labels[user_name+".txt"]
            except:
                index = filename.rfind("/")
                user_name = filename[index+1:].strip()
                label = self.labels[user_name]
            profile_pic = f.readline().strip()
            #Go over all tweets of the user
            tweets,retweet_count = self.file_to_list(f)
            for line in tweets:
                self.get_features(line)
            tweet_count = len(tweets)
            self.socling.max_values["TWEETS"] = tweet_count
            self.socling.features_dict["RETWEETS"] = retweet_count/tweet_count
            #Check if all features are accounted for
            self.socling.check_dict(self.features_list)
            #self.socling.normalizer()
            #Write features to file for user
            #print(label)
            for i,feature in enumerate(self.features_list):
                output.write(str(float(self.features[feature]))+"\t")
            output.write("||"+label+"\n")
            #output.write("\n")



start = time.time()
c = Classifier()
print("Preprocessing")
#c.create_features_list()
file_type = "train"
demographic = "age"
c.initialize()
print("Training")
c.features_svm(file_type,demographic)
print("Testing")
file_type = "test"
c.features_svm(file_type,demographic)
print("Running Logistic Regression")
c.logistic_regression(demographic)
end = time.time()
print end-start
