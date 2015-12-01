from SocioLinguistic import SocioLinguistic
import get_age_or_gender
import glob
import time

class Classifier:
    def __init__(self):
        self.socling = SocioLinguistic()
        self.features_list = []
        self.features = {}
        self.labels = {}

    def label_file_to_dict(self,filename):
        dict_x = {}
        for line in open(filename,"r"):
            # print line
            temp = line.split("||")
            name = temp[0].strip()
            label = temp[1].strip()
            if label == "FEMALE":
                label = "0"
            else:
                label = "1"
            dict_x[name] = label
        return dict_x

    def create_features_list(self):
        self.socling.sent = "Some sentence"
        self.features_list.extend(self.socling.emoticons())
        self.features_list.extend(self.socling.excitement())
        self.features_list.extend(self.socling.single_exclam())
        self.features_list.extend(self.socling.ellipses())
        self.features_list.extend(self.socling.possessive_bigrams())
        self.features_list.extend(self.socling.pumping())
        self.features_list.extend(self.socling.self())
        self.features_list.extend(self.socling.laugh())
        self.features_list.extend(self.socling.shout())
        self.features_list.extend(self.socling.exasperation())
        self.features_list.extend(self.socling.agreement())
        self.features_list.extend(self.socling.honorifics())
        self.features_list.extend(self.socling.affection())
        print self.features_list
        f = open("feature_files/feature_names","w")
        for feature in self.features_list:
            f.write(feature+"\n")
        f.close()


    def get_features(self,line):
        self.socling.sent = line
        self.socling.emoticons()
        self.socling.excitement()
        self.socling.single_exclam()
        self.socling.ellipses()
        self.socling.possessive_bigrams()
        self.socling.pumping()
        self.socling.self()
        self.socling.laugh()
        self.socling.shout()
        self.socling.exasperation()
        self.socling.agreement()
        self.socling.honorifics()
        self.socling.affection()

    def features_svm(self,file_type):
        self.labels = self.label_file_to_dict("../all_labels.txt")
        self.features_list = self.socling.file_to_list("feature_files/feature_names")
        files = []
        output = open("svm/"+file_type+"_file","w")
        for filename in glob.glob("../gend_"+file_type+"_reduced/*.txt"):
            #Reset dictionary for every user
            self.socling.features_dict = self.features
            f = open(filename,"r")
            user_name = f.readline().strip()
            #print user_name
            label = self.labels[user_name+".txt"]
            output.write(label+"\t")
            profile_pic = f.readline().strip()
            #Go over all tweets of the user
            for line in f:
                self.get_features(line)
            f.close()
            #Check if all features are accounted for
            self.socling.check_dict(self.features_list)
            #Write features to file for user
            for i,feature in enumerate(self.features_list):
                output.write(str(i)+":"+str(self.features[feature])+"\t")
            output.write("\n")
            #Reset dictionary for every user
            self.features = {}

start = time.time()
c = Classifier()
c.features_svm("train")
end = time.time()
print end-start
