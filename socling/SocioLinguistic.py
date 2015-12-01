from nltk import word_tokenize,bigrams
import re
class SocioLinguistic:
    def __init__(self):
        self.emoji = self.file_to_list("feature_files/baseline_emoticons.txt")
        self.sent = ""
        self.features_dict = {}

    def file_to_list(self,filename):
        list_x = []
        for line in open(filename,"r"):
            # print line
            x = line.split("\t")[0].strip()
            list_x.append(str(x))
        return list_x

    def emoticons(self,sent,features_dict):
        for emo in self.emoji:
            if sent.find(emo) > -1:
                features_dict[emo] = 1
            else:
                features_dict[emo] = 0
        return self.emoji

    def check_dict(self,features_list):
        for word in features_list:
            if word not in self.features_dict:
                self.features_dict[word] = 0

    def excitement(self):
        sent_list = word_tokenize(self.sent.lower())
        features_list = ["OMG","EXC_EXCLAM","EXC_PUZZLED"]
        if "omg" in sent_list:
            self.features_dict["OMG"] = 1
        count = 0
        question = False
        for c in self.sent:
            if c == "!":
                count +=1
            elif c == "?":
                question = True
                count += 1
            else:
                if count > 2:
                    if question:
                        self.features_dict["EXC_PUZZLED"] = 1
                    else:
                        self.features_dict["EXC_EXCLAM"] = 1
        self.check_dict(features_list)
        return features_list

    def single_exclam(self):
        feature = "EXCLAM"
        count = 0
        sent = self.sent.strip()
        if len(sent) > 1 and sent[-1] == "!" and sent[-2] != sent:
            self.features_dict[feature] = 1
        self.check_dict([feature])
        return [feature]

    def check_repeat(self,check_char):
        count = 0
        for c in self.sent:
            if c == check_char:
                count += 1
            else:
                if count > 2:
                    return True
                count = 0
        return False

    def ellipses(self):
        count = 0
        feature = "ELLIPSES"
        for c in self.sent:
            count = self.check_match(c,".",count)
            if count == "success":
                self.features_dict[feature] = 1
                return [feature]
        self.check_dict([feature])
        return [feature]

    def possessive_bigrams(self):
        features_list = ["MY","YOUR","HIS","HER","OUR","THEIR"]
        sent_bigrams = bigrams(word_tokenize(self.sent))
        for pair in sent_bigrams:
            key = pair[0].upper()
            if key in features_list:
                self.features_dict[key] = 1
        self.check_dict(features_list)
        return features_list

    def check_match(self,a,b,count):
        if a == b:
            count += 1
            return count
        else:
            if count > 2:
                return "success"
            return 0

    def pumping(self):
        feature = "PUMPING"
        count = 0
        prev = self.sent[0]
        for c in self.sent[1:]:
            if c.isalpha():
                count = self.check_match(c,prev,count)
                if count == "success":
                    self.features_dict[feature] = 1
                    return [feature]
            prev = c

    def self(self):
        features_list = ["I","IM","I'M","ILL","I'LL","I'VE","IVE","ID","I'D"]
        sent_list = self.sent.upper().split()
        for word in sent_list:
            if word in features_list:
                self.features_dict[word] = 1
        self.check_dict(features_list)
        return features_list


    def laugh(self):
        features_list = ["LOL","ROFL","LMAO"]
        sent_list = word_tokenize(self.sent.upper())
        for word in sent_list:
            if word in features_list:
                self.features_dict[word] = 1
        self.check_dict(features_list)
        return features_list

    def shout(self):
        feature = "SHOUT"
        if self.sent.isupper():
            self.features_dict[feature] = 1
        self.check_dict([feature])
        return [feature]

    def exasperation(self):
        features_list = ["UGH","MM","HM","AHH","GRR"]
        sent_list = word_tokenize(self.sent.upper())
        for word in sent_list:
            for feature in features_list:
                if re.match(feature+".*",word) is not None:
                    self.features_dict[feature] = 1
        self.check_dict(features_list)
        return features_list

    def agreement(self):
        features_list = ["YES","YEAH","YEA","YUP","OHYA"]
        self.check_belonging(features_list)
        return features_list

    def check_belonging(self,features_list):
        sent_list = word_tokenize(self.sent.upper())
        for word in sent_list:
            if word in features_list:
                self.features_dict[word] = 1
        self.check_dict(features_list)

    def honorifics(self):
        features_list = ["DUDE","BRO","MAN","MA'AM","MADAM"]
        self.check_belonging(features_list)
        return features_list

    def affection(self):
        features_list = ["XOXO"]
        self.check_belonging(features_list)
        return features_list










