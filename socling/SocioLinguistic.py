from nltk import word_tokenize,bigrams
import re
import glob
import enchant
class SocioLinguistic:
    def __init__(self):
        self.emoji = set(self.file_to_list("feature_files/emoticons"))
        self.emoticons_unicode = set(self.file_to_list("feature_files/emoticons_unicode"))
        self.sent = ""
        self.features_dict = {}
        self.max_values = {}
        self.max_values["EMOTICON"] = 1.0 #default
        self.sent_list = []
        self.english = enchant.Dict("en")

    def file_to_list(self,filename):
        list_x = []
        for line in open(filename,"r"):
            ## print line
            x = line.split("\t")[0].strip()
            list_x.append(x)
        return list_x

    def emoticons(self):
        for word in self.sent_list:
            word_utf = word.encode("utf-8")
            if word_utf in self.emoji:
                #print("Emoticons:",self.sent_list)
                #self.features_dict[word_utf] += 1.0
                self.features_dict[word_utf] = 1.0
                self.max_values["EMOTICON"] += 1.0
        return self.emoji

    def normalizer(self):
        for emo in self.emoji:
            try:
                self.features_dict[emo] = self.features_dict[emo] / self.max_values["EMOTICON"]
            except:
                self.features_dict[emo] = 0.0
            ##print emo, self.features_dict[emo]
        #Single_exclamation
        self.features_dict["EXCLAM"] /= self.max_values["TWEETS"]
        #Shout
        self.features_dict["SHOUT"] /= self.max_values["TWEETS"]
        ##print self.features_dict["EXCLAM"]

    def check_dict(self,features_list):
        for word in set(features_list):
            if word not in self.features_dict:
                self.features_dict[word] = 0

    def excitement(self):
        features_list = ["OMG","EXC_EXCLAM","EXC_PUZZLED"]
        if "OMG" in self.sent_list:
            #print("OMG:",self.sent)
            self.features_dict["OMG"] = 1
            #self.features_dict["OMG"] += 1/float(len(self.sent.split()))
        sent_list = self.sent.split()
        #normalizer = len(sent_list)
        normalizer = 1
        count = len(re.findall("!!!*",self.sent))
        if count > 0:
            #print("Excitement!!!:",self.sent)
            #self.features_dict["EXC_EXCLAM"] += count
            #self.features_dict["EXC_EXCLAM"] += count/normalizer
            self.features_dict["EXC_EXCLAM"] = 1
        else:
            count = len(re.findall("[?!]*![?!]*",self.sent))
            if count > 0:
                #print("Puzzled:",self.sent)
                #self.features_dict["EXC_PUZZLED"] += count/normalizer
                #self.features_dict["EXC_PUZZLED"] += count
                self.features_dict["EXC_PUZZLED"] = 1
        return features_list

    def single_exclam(self):
        feature = "EXCLAM"
        count = 0
        sent = self.sent.strip()
        if len(sent) > 1 and sent[-1] == "!" and sent[-2] != sent:
            ##print sent
            #print("Single exclamation:",self.sent)
            self.features_dict[feature] += 1
        return [feature]

    def ellipses(self):
        count = 0
        feature = "ELLIPSES"
        if "..." in self.sent_list:
            #print("Ellipses:",self.sent)
            #self.features_dict[feature] += self.sent_list.count("...")
            #self.features_dict[feature] += self.sent_list.count("...")/len(self.sent_list)
            self.features_dict[feature] = 1
        return [feature]

    def create_possessive_bigrams(self):
        possessive_list = {"MY","YOUR","HIS","HER","OUR","THEIR"}
        self.possessive_bigram = set()
        i = 0
        for filename in glob.glob("../gend_train/*.txt"):
            i += 1
            #print i
            for line in open(filename,"r"):
                if line.strip() == '' or line[:1] == "RT":
                    continue
                sent_list = word_tokenize(line.upper().strip().decode("utf-8"))
                sent_bigram = bigrams(sent_list)
                for pair in sent_bigram:
                    if pair[0] in possessive_list:
                        self.possessive_bigram.add(pair[0]+"_"+pair[1])
        return self.possessive_bigram

    def possessive_bigrams(self,features_list):
        flag = False
        possessive_list = {"MY","YOUR","HIS","HER","OUR","THEIR","YO"}
        for word in self.sent_list:
            if word in possessive_list:
                flag = True
        if flag:
            sent_bigrams = bigrams(self.sent_list)
            len_bigram = sent_bigrams.__sizeof__()
            for pair in sent_bigrams:
                key = pair[0]+"_"+pair[1]
                if key in features_list:
                    self.features_dict[key] = 1
                    #self.features_dict[key] += 1/float(len_bigram)
                    #self.features_dict[key] += 1
                    #print("Possessive bigram:",self.sent)

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
        pumping = re.findall("([a-z])\\1\\1",self.sent.lower())
        if len(pumping) > 0:
            #print("Pumping:",self.sent)
            self.features_dict[feature] = 1
            #self.features_dict[feature] += 1/float(len(self.sent_list))
            #self.features_dict[feature] += 1
        return [feature]

    def self(self):
        features_list = ["I"]
        sent_list = word_tokenize(self.sent.upper().decode("utf-8"))
        count = sent_list.count("I")
        if count > 0:
            #print("I:",self.sent)
            #self.features_dict["I"] += count/float(len(sent_list))
            #self.features_dict["I"] += count
            self.features_dict["I"] = 1
        return features_list

    def slang(self):
        feature = "SLANG"
        for word in self.sent_list:
            if word.isalpha():
                if not self.english.check(word):
                    #self.features_dict["SLANG"] += 1.0/len(self.sent_list)
                    self.features_dict["SLANG"] = 1

    def laugh(self):
        features_list = {"LOL","ROFL","LMAO","LMFAO","HAHA","HEHE"}
        length = len(self.sent_list)
        for word in features_list:
            count = len(re.findall(word,self.sent.upper()))
            if count > 0:
                #print("Laugh:",self.sent)
                #self.features_dict[word] += count/float(length)
                self.features_dict[word] = 1
                #self.features_dict[word] += count
        return features_list

    def shout(self):
        #Normalized in normalizer()
        feature = "SHOUT"
        if self.sent.isupper():
            #print("Shout:",self.sent)
            #self.features_dict[feature] += 1
            self.features_dict[feature] = 1
        return [feature]

    def exasperation(self):
        features_list = {"UGH", "MM", "HM", "AHH", "GRR"}
        length = len(self.sent_list)
        for word in features_list:
            count = len(re.findall(word,self.sent.upper()))
            if count > 0:
                #print("Exasperation:",self.sent)
                #self.features_dict[word] += count/float(length)
                self.features_dict[word] = 1
                #self.features_dict[word] += count
        return list(features_list)

    def agreement(self):
        features_list = {"YES", "YEAH", "YEA", "YUP", "OHYA"}
        length = len(self.sent_list)
        for word in features_list:
            count = len(re.findall(word,self.sent.upper()))
            if count > 0:
                #print("Agreement:",self.sent)
                #self.features_dict[word] += count/float(length)
                self.features_dict[word] = 1
                #self.features_dict[word] += count
        return features_list

    def honorifics(self):
        features_list = {"DUDE","BRO","MAN","MA'AM","MADAM"}
        for word in self.sent_list:
            if word in features_list:
                #print("Honorifics:",self.sent.upper())
                #self.features_dict[word] += 1/len(self.sent_list)
                self.features_dict[word] = 1
        return list(features_list)

    def affection(self):
        features_list = {"XO","PLEASE","THANK","AWW"}
        length = len(self.sent_list)
        for word in features_list:
            count = len(re.findall(word,self.sent.upper()))
            if count > 0:
                #print("Affection:",self.sent)
                #self.features_dict[word] += count/float(length)
                self.features_dict[word] = 1
                #self.features_dict[word] += count
        return list(features_list)