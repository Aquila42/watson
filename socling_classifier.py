from SocioLinguistic import SocioLinguistic
from tweetokenize import Tokenizer

class SocioLinguisticClassifier:
    def __init__(self):
        self.socling = SocioLinguistic()
        self.features_list = []
        self.features = {}
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

    def initialize(self,demographic):
        self.features_list = set(self.socling.file_to_list("feature_files/feature_names_" + demographic))

    def reset_dictionary(self):
        self.features = {}
        for feature in self.features_list:
            self.features[feature] = 0

    def stacked_socling_init(self,demographic):
        self.features_list = set(self.socling.file_to_list("feature_files/feature_names_" + demographic))
        self.reset_dictionary()
        self.socling.features_dict = self.features
