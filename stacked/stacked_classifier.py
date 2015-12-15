from socling_classifier import SocioLinguisticClassifier
from unigram_classifer import unigramClassifier
from bigram_classifier import bigramClassifier
from genderPredictor import genderPredictor
import pickle

class StackedClassifier:
    def __init__(self,handle,name):
        self.name = name
        self.handle = handle
        print(self.name,self.handle)
        self.socling = SocioLinguisticClassifier()
        self.unigram = unigramClassifier()
        self.bigram = bigramClassifier()
        self.features_gend = []
        self.features_age = []

    def get_labels(self):
        self.run_stacked()
        gender = self.predict_label(demographic="gend",features_list=self.features_gend)
        age = self.predict_label(demographic="age",features_list=self.features_age)
        if age == "under25":
            age = "Under 25"
        print(gender,age)
        return gender,age

    def predict_label(self,demographic,features_list):
        #Unpickle objects
        with open('chi_squared_'+demographic+'.pkl', 'rb') as input:
            ch2 = pickle.load(input)
        features_list = ch2.transform(features_list)
        with open('trained_classifier_'+demographic+'.pkl', 'rb') as input:
            clf = pickle.load(input)
        predicted = clf.predict(features_list)
        return predicted[0]

    def get_features_list(self,demographic):
        self.tweets = open(self.handle+".txt")
        self.socling.stacked_socling_init(demographic)
        self.tweets.readline().strip() #twitter handle
        self.tweets.readline().strip() #profile picture
        features_list = []
        for line in self.tweets:
            self.socling.get_features(line,demographic)
            self.unigram.buildSet(line)
            self.bigram.buildSet(line)
        #Socling features dictionary created
        #Ngram dictionary created
        for item in self.unigram.unigrams_dictionary:
            features_list.append(self.unigram.unigrams_dictionary[item])
        for item in self.bigram.bigrams_dictionary:
            features_list.append(self.bigram.bigrams_dictionary[item])
        for item in self.socling.features:
            features_list.append(self.socling.features[item])
        return features_list

    def run_stacked(self):
        demographic = "gend"
        self.socling.stacked_socling_init(demographic)
        self.unigram.createDictionary(demographic)
        self.bigram.createDictionary(demographic)
        self.features_gend = self.get_features_list(demographic)
        gender_prediction = genderPredictor().getGender(self.name)
        if str(gender_prediction)=='0':
            self.features_gend.extend([1,0,0])
        elif str(gender_prediction)=='1':
            self.features_gend.extend([0,1,0])
        else:
            self.features_gend.extend([0,0,1])
        demographic = "age"
        self.socling.stacked_socling_init(demographic)
        self.unigram.createDictionary(demographic)
        self.bigram.createDictionary(demographic)
        self.features_age = self.get_features_list(demographic)

# stacked = StackedClassifier("215__chris","Chris")
# print(stacked.get_labels())
