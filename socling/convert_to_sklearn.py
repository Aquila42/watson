from sklearn import svm
file_type = "train"
input_file = open("svm/"+file_type+"_file","r")
output_file = open("svm/sk_"+file_type,"w")
features = []
labels = []
i = 0
for line in input_file:
    i+=1
    print(i)
    temp = line.strip().split("\t")
    label = temp[0]
    if label == "0":
        label = "FEMALE"
    else:
        label = "MALE"
    labels.append(label)
    temp_list = []
    for feature in temp[1:]:
        value = feature.split(":")[1]
        temp_list.append(value)
        output_file.write(str(value)+"\t")
    features.append(temp_list)
    output_file.write("|| "+label+"\n")
