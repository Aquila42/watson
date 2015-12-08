import glob
import re

def file_to_list(filename):
    list_x = []
    for line in open(filename,"r"):
        x = line.strip().split("\t")[0]
        list_x.append(str(x))
    return list_x

file_type = "train"
#emoji = set(file_to_list("feature_files/baseline_emoticons"))
emoji_dict = {}
i = 0
for filename in glob.glob("../gend_"+file_type+"/*.txt"):
    print(i)
    i += 1
    for line in open(filename):
            if emo in line:
                print(line)
                if emo in emoji_dict:
                    emoji_dict[emo] += line.count(emo)
                else:
                    emoji_dict[emo] = line.count(emo)
print(emoji_dict)
'''
f = open("feature_files/emoticons_common_final","w")
for emo in emoji_dict:
    f.write(emo+"\t"+str(emoji_dict[emo])+"\n")
f.close()
'''