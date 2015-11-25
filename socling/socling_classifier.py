from SocioLinguistic import SocioLinguistic
import get_age_or_gender
import glob

class Classifier:
    def __init__(self):
        self.socling = SocioLinguistic()
        self.features_list = []
        self.features = {}

    def get_features(self):
        svm = open("svm_output","w")
        files = open("people","w")
        for filename in glob.glob("../data/*.txt"):
            print filename
            f = open(filename,"r")
            name = f.readline()
            url = f.readline().strip()
            try:
                value = get_age_or_gender.get_demographic(url,"gender")
            except:
                continue
            if value != -1:
                for line in f:
                    sent = line.strip()
                    self.features_list.extend(self.socling.emoticons(sent,self.features))
                for feature in self.features_list:
                    svm.write(str(self.features[feature])+"\t")
                svm.write("|| "+value.upper()+"\n")
                files.write(filename+" || "+value+"\n")

c = Classifier()
c.get_features()