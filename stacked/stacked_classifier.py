from socling.socling_classifier import SocioLinguisticClassifier
import pickle
class StackedClassifier:
    def __init__(self,handle,name):
        self.name = name
        self.handle = handle
        self.socling = SocioLinguisticClassifier()
        # self.unigram = unigramClassifier()
        # self.bigram = bigramClassifier()
        self.features_gend = []
        self.features_age = []
        self.gender = ""
        self.age = ""

    def get_labels(self):
        self.run_stacked()
        with open('chi_squared.pkl', 'rb') as input:
            ch2 = pickle.load(input)
        ch2.transform(self.features)
        with open('trained_classifier.pkl', 'rb') as input:
            clf = pickle.load(input)
        clf.predict(self.features)
        #Unpickle objects
        #ch2.transform(features)
        #clf.predict(features) #Gender
        #return gender,age # {gender:"FEMALE",age:"under25"}

    def reset(self):
        self.tweets = open(self.handle+".txt")
        self.socling.stacked_socling_init()
        self.tweets.readline().strip() #twitter handle
        self.tweets.readline().strip() #profile picture

    def get_features_list(self,demographic):
        self.reset()
        features_list = []
        for line in self.tweets:
            self.socling.get_features(line,demographic)
            #self.unigram.buildSet()
            #self.bigram.buildSet()
        #Socling features dictionary created
        #Ngram dictionary created
        '''
        for item in self.unigram.unigrams_dictionary:
            self.features_list.append(self.unigram.unigrams_dictionary[item])
        for item in self.bigram.bigrams_dictionary:
            self.features_list.append(self.bigram.bigrams_dictionary[item])
        for item in self.socling.features:
            self.features_list.append(self.socling.features[item])
        '''
        return features_list

    def run_stacked(self):
        self.features_gend = self.get_features_list("gend")
        # genderPrediction = genderPredictor().getGender(name)
        # if str(genderPrediction)=='0':
        #     self.features_gend.extend([1,0,0])
        # elif str(genderPrediction)=='1':
        #     self.features_gend.extend([0,1,0])
        # else:
        #     self.features_gend.extend([0,0,1])

        self.features_age = self.get_features_list("age")