from nltk import NaiveBayesClassifier,classify
import USSSALoader
import random

class genderPredictor():
    
    def getFeatures(self):
        maleNames,femaleNames=self._loadNames()
        
        featureset = list()
        for nameTuple in maleNames:
            features = self._nameFeatures(nameTuple[0])
            featureset.append((features,'M'))
        
        for nameTuple in femaleNames:
            features = self._nameFeatures(nameTuple[0])
            featureset.append((features,'F'))
    
        return featureset
    
    def trainAndTest(self,trainingPercent=0.80):
        featureset = self.getFeatures()
        random.shuffle(featureset)
        
        name_count = len(featureset)
        
        cut_point=int(name_count*trainingPercent)
        
        train_set = featureset[:cut_point]
        test_set  = featureset[cut_point:]
        
        self.train(train_set)
        
        return self.test(test_set)
        
    def classify(self,name):
        feats = self._nameFeatures(name)
        return self.classifier.classify(feats)
        
    def train(self,train_set):
        self.classifier = NaiveBayesClassifier.train(train_set)
        return self.classifier
        
    def test(self,test_set):
       return classify.accuracy(self.classifier,test_set)
        
    def getMostInformativeFeatures(self,n=5):
        return self.classifier.most_informative_features(n)
        
    def _loadNames(self):
        return USSSALoader.getNameList()
        
    def _nameFeatures(self,name):
        name=name.upper()
        return {
            'last_letter': name[-1],
            'last_two' : name[-2:],            
            'last_is_vowel' : (name[-1] in 'AEIOUY')
        }

    def getGender(self,name):
        self.trainAndTest()
        if name == '###FOREIGN###' or name == '###EMOTICON###':
            return '2'
        else:
            return self.classify(str(name))
