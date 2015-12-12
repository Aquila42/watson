from sklearn import cross_validation,linear_model,metrics
from sklearn.cross_validation import StratifiedKFold
import numpy as np

def features_from_file(f):
    features = []
    labels = []
    for line in f:
        temp = line.strip().split("||")
        feature = temp[0].strip().split()
        label = temp[1].strip()
        features.append(np.array(feature).astype(float))
        labels.append(label)
    return features,labels
demographic = "manual_age_200"
train = open("svm/"+demographic,"r")
# train = open("svm/"+demographic+"_train","r")
features,labels = features_from_file(train)
clf = linear_model.LogisticRegression(C=0.01)
# clf = linear_model.Perceptron()
skf = StratifiedKFold(labels, 10)
print(labels)
accuracy = []
for train,test in skf:
    X_train = []
    y_train = []
    X_test = []
    y_test = []
    for i in train:
        X_train.append(features[i])
        y_train.append(labels[i])
    for i in test:
        X_test.append(features[i])
        y_test.append(labels[i])
    clf.fit(X_train, y_train)
    predicted = clf.predict(X_test)
    accuracy.append(metrics.accuracy_score(predicted,y_test))
print reduce(lambda x, y: x + y, accuracy) / len(accuracy)
