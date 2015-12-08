from sklearn import svm, metrics, linear_model, tree
import numpy as np

def features_from_file(f):
    features = []
    labels = []
    for line in f:
        temp = line.strip().split("||")
        feature = temp[0].strip().split("\t")
        label = temp[1].strip()
        features.append(np.array(feature).astype(float))
        labels.append(label)
    return features,labels

train = open("svm/age_train","r")
test = open("svm/age_test","r")

train_features,train_labels = features_from_file(train)
test_features,test_labels = features_from_file(test)

#print(train_features,train_labels)

clf = svm.SVC(gamma=0.001,C=100.)
clf.fit(train_features, train_labels)
predicted = clf.predict(test_features)
print("SVM:",metrics.accuracy_score(predicted,test_labels))

clf = linear_model.LogisticRegression()
clf.fit(train_features, train_labels)
predicted = clf.predict(test_features)
print("Logistic Regression:",metrics.accuracy_score(predicted,test_labels))

clf = tree.DecisionTreeClassifier()
clf = clf.fit(train_features,train_labels)
predicted = clf.predict(test_features)
print("Decision Tree:",metrics.accuracy_score(predicted,test_labels))

clf = linear_model.Perceptron(n_iter=10)
clf.fit(train_features, train_labels)
predicted = clf.predict(test_features)
print("Perceptron:",metrics.accuracy_score(predicted,test_labels))
