from SocioLinguistic import SocioLinguistic
from sklearn import linear_model, metrics
# from nltk import word_tokenize
from tweetokenize import Tokenizer
import get_age_or_gender
import glob
import time
import numpy as np
import re


class SocioLinguisticClassifier:
    def __init__(self):
        self.socling = SocioLinguistic()
        self.features_list = []
        self.features = {}
        self.labels = {}
        self.gettokens = Tokenizer()

    def label_file_to_dict(self, filename):
        dict_x = {}
        for line in open(filename, "r"):
            # print line
            temp = line.split("||")
            name = temp[0].strip()
            label = temp[1].strip()
            dict_x[name] = label
        return dict_x

    def create_features_list(self, demographic):
        self.socling.sent = "Some sentence"
        if demographic == "gend":
            self.features_list.extend(self.socling.single_exclam())
            self.features_list.extend(self.socling.pumping())
            self.features_list.extend(self.socling.agreement())
            self.features_list.extend(self.socling.affection())
        self.features_list.extend(self.socling.emoticons())
        self.features_list.extend(self.socling.excitement())
        self.features_list.extend(self.socling.ellipses())
        self.features_list.extend(self.socling.laugh())
        self.features_list.extend(self.socling.slang())
        self.features_list.extend(self.socling.shout())
        self.features_list.extend(self.socling.exasperation())
        self.features_list.extend(self.socling.honorifics())
        self.features_list.extend(self.socling.pronouns())
        self.features_list.extend(self.socling.standard_english())
        self.features_list.extend(self.socling.school())
        self.features_list.extend(["RETWEETS"])
        self.features_list.extend(self.socling.create_possessive_bigrams("../" + demographic + "_train/*.txt"))
        f = open("feature_files/feature_names_" + demographic, "w")
        for feature in self.features_list:
            try:
                f.write(feature + "\n")
            except:
                continue
        f.close()

    def get_features(self, line, demographic):
        self.socling.sent = line
        self.socling.sent_list = self.gettokens.tokenize(line.upper())
        if demographic == "gend":
            self.socling.single_exclam()
            self.socling.pumping()
            self.socling.agreement()
            self.socling.affection()
        self.socling.emoticons()
        self.socling.excitement()
        self.socling.ellipses()
        self.socling.possessive_bigrams(self.features_list)
        self.socling.laugh()
        self.socling.shout()
        self.socling.exasperation()
        self.socling.honorifics()
        self.socling.slang()
        self.socling.pronouns()

    def reset_dictionary(self):
        for feature in self.features_list:
            self.features[feature] = 0

    def file_to_list(self, f):
        tweets = []
        retweets = 0
        for line in f:
            if line.strip() == "":
                continue
            elif "RT" in line.strip()[:1]:
                retweets += 1
            else:
                line = re.sub('https?:\/\/.*[\r\n]*', '', line)
                # print(line)
                tweets.append(line.strip())
        f.close()
        return tweets, retweets

    def features_from_file(self, f):
        features = []
        labels = []
        for line in f:
            temp = line.strip().split("||")
            feature = temp[0].strip().split("\t")
            label = temp[1].strip()
            features.append(np.array(feature).astype(float))
            labels.append(label)
        return features, labels

    def logistic_regression(self, demographic):
        train = open("svm/" + demographic + "_train", "r")
        test = open("svm/" + demographic + "_test", "r")
        train_features, train_labels = self.features_from_file(train)
        test_features, test_labels = self.features_from_file(test)
        clf = linear_model.LogisticRegression(C=0.001)
        clf.fit(train_features, train_labels)
        predicted = clf.predict(test_features)
        print(predicted)
        print("Logistic Regression:", metrics.accuracy_score(predicted, test_labels))

    def stacked_socling_init(self):
        self.reset_dictionary()
        self.socling.features_dict = self.features
        self.labels = self.label_file_to_dict("../all_labels_" + demographic + ".txt")
        self.features_list = set(self.socling.file_to_list("feature_files/feature_names_" + demographic))

    def features_svm(self, file_type, demographic):
        output = open("svm/" + demographic + "_" + file_type, "w")
        j = 0
        for filename in glob.glob("../" + demographic + "_" + file_type + "/*.txt"):
            self.reset_dictionary()
            self.socling.features_dict = self.features
            f = open(filename, "r")
            user_name = f.readline().strip()
            try:
                label = self.labels[user_name + ".txt"]
            except:
                index = filename.rfind("/")
                user_name = filename[index + 1:].strip()
                label = self.labels[user_name]
            if label == "":
                print(user_name)
                break
            print(j)
            j += 1
            profile_pic = f.readline().strip()
            # Go over all tweets of the user
            tweets, retweet_count = self.file_to_list(f)
            for line in tweets:
                self.get_features(line, demographic)
            # Check if all features are accounted for
            for i, feature in enumerate(self.features_list):
                output.write(str(float(self.features[feature])) + "\t")
            output.write("|| " + label + "\n")
            # print(count_over,count_under)
            # print(j)


start = time.time()
c = SocioLinguisticClassifier()
print("Preprocessing")
demographic = "gend"
c.create_features_list(demographic)
c.stacked_socling_init()
print("Training")
file_type = "train"
c.features_svm(file_type, demographic)
print("Testing")
file_type = "test"
# c.features_svm(file_type,demographic)
print("Running Logistic Regression")
# c.logistic_regression(demographic)
end = time.time()
print end - start
