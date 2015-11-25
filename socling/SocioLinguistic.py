class SocioLinguistic:
    def __init__(self):
        self.emoji = self.file_to_list("feature_files/baseline_emoticons.txt")

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