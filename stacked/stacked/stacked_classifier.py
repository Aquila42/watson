# -*- coding: utf-8 -*-

import copy
import glob
import nltk
import re
from sklearn import svm
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import Perceptron
from sklearn.linear_model import LogisticRegression
from sklearn.linear_model import RandomizedLasso
from sklearn.feature_selection import SelectKBest, chi2
from sklearn.tree import DecisionTreeClassifier
import numpy as np
from nltk import word_tokenize
from operator import itemgetter
import pickle


def main():
    # soc_train = 'soc_train.txt'
    # soc_test = 'soc_test.txt'

    ngram_train2 = 'cv_bigrams_new100.txt'
    # ngram_test2 = 'test_set_bigrams_binary.txt'
    ngram_train = 'cv_unigrams_new100.txt'
    # ngram_test = 'ngram_test.txt'
    soc_train = 'cv_soc_new100.txt'
    # soc_test = 'soc_test.txt'

    # genderLabels = createLabelsDict()
    # combineFiles(soc_train, ngram_train, ngram_train2, 'train', genderLabels)
    combineFiles(soc_train, ngram_train, ngram_train2, 'train')
    # combineFiles(soc_test,ngram_test,ngram_test2,'test',genderLabels)
    clf, ch2 = trainClassifier()
    with open('../trained_classifier_age.pkl', 'wb') as output:
        pickle.dump(clf, output, pickle.HIGHEST_PROTOCOL)
    with open('../chi_squared_age.pkl', 'wb') as output:
        pickle.dump(ch2, output, pickle.HIGHEST_PROTOCOL)


    # (results,y_test) = predict(clf,ch2)
    # getAccuracy(results,y_test)


def createLabelsDict():
    # f = open('../genderLabels_new.txt','r')
    f = open('../genderLabels.txt', 'r')
    f_line = f.readline()
    genderLabels = dict()
    while f_line:
        f_line_split = f_line.split()
        if str(f_line_split[1]) == 'M':
            val = 0
        elif str(f_line_split[1]) == 'F':
            val = 1
        else:
            val = 2
        genderLabels[str(f_line_split[0])] = str(val)
        f_line = f.readline()
    return genderLabels


def combineFiles(soc, ngram, ngram2, datatype, genderLabels=None):
    print "Combining feature sets"
    if datatype == 'train':
        data_set = open('train_set_2000.txt', 'w')
        all_labels_file = open("../all_training_file_names2.txt", 'r')
    else:
        data_set = open('test_set_unigrams.txt', 'w')
        all_labels_file = open("../all_test_file_names.txt", 'r')
    label_line = all_labels_file.readline()
    f_soc = open(soc)
    line_soc = f_soc.readline()
    f_ngram = open(ngram)
    line_ngram = f_ngram.readline()
    f_ngram2 = open(ngram2)
    line_ngram2 = f_ngram2.readline()
    while line_ngram:
        string = ''
        line_ngram_split = line_ngram.split('||')
        line_ngram_split2 = line_ngram2.split('||')
        line_soc_split = line_soc.split('||')
        if str(line_ngram_split[1].strip()) != str(line_soc_split[1].strip()):
            print str(line_ngram_split[1].strip()), " ", str(line_soc_split[1].strip())
            print "Labels do not match"
        string = str(line_ngram_split[0].strip()) + " " + str(line_ngram_split2[0].strip()) + " " + str(line_soc_split[0].strip())
        # string = str(line_ngram_split[0].strip()) + " "
        # gender_pred = genderLabels[str(label_line.strip())]
        # if str(gender_pred) == '0':
        #     gender_pred = '1 0 0'
        # elif str(gender_pred) == '1':
        #     gender_pred = '0 1 0'
        # else:
        #     gender_pred = '0 0 1'
        # string += str(gender_pred)
        string += " || " + str(line_ngram_split[1].strip()) + "\n"
        data_set.write(string)
        line_soc = f_soc.readline()
        line_ngram = f_ngram.readline()
        line_ngram2 = f_ngram2.readline()
        label_line = all_labels_file.readline()
    data_set.close()


def trainClassifier():
    # Train classifier
    print "Training classifier"
    # Linear SVM C = 1
    y_train = []
    x_train = []
    # training_set = open('ngram_train.txt')
    training_set = open('train_set_2000.txt')
    line = training_set.readline()
    count = 0
    while line:
        count += 1
        print count
        line_split = line.split()
        x_train_per_user = []
        for feature in line_split:
            if (feature != '||' and feature != 'under25' and feature != '25+'):
                x_train_per_user.append(float(feature))
            if (feature == 'under25' or feature == '25+'):
                y_train.append(feature)
        x_train.append(x_train_per_user)
        line = training_set.readline()
    print len(x_train[0])
    print len(y_train)
    # clf = svm.SVC(kernel='linear', C = 1)
    clf = LogisticRegression(C=0.01)
    # clf = Perceptron(n_iter=10)
    # clf = KNeighborsClassifier(n_neighbors=25)
    # clf = RandomForestClassifier(n_estimators=100)
    # clf = svm.SVC(kernel='rbf', C = 100, gamma=0.01)
    # clf = DecisionTreeClassifier(random_state=0)
    # clf = svm.SVC(kernel='poly', C=1,degree=4)

    # print sorted(zip(map(lambda x: round(x, 4), rlasso.scores_),
    #                 names), reverse=True)

    print "Getting k best features"
    ch2 = SelectKBest(chi2, 'all')
    # ch2 = SelectKBest(chi2, 55000)
    x_train = ch2.fit_transform(x_train, y_train)
    print len(x_train[0])

    print "Fitting"
    clf.fit(x_train, y_train)
    # return clf
    return (clf, ch2)


def predict(clf, ch2):
    # Test
    print "Predicting"
    y_test = []
    x_test = []
    # test_set = open('ngram_test.txt')
    test_set = open('test_set_unigrams.txt')
    line = test_set.readline()
    while line:
        line_split = line.split()
        x_test_per_user = []
        for feature in line_split:
            if (feature != '||' and feature != 'MALE' and feature != 'FEMALE'):
                x_test_per_user.append(float(feature))
            if (feature == 'MALE' or feature == 'FEMALE'):
                y_test.append(feature)
        x_test.append(x_test_per_user)
        line = test_set.readline()

    x_test = ch2.transform(x_test)

    results = clf.predict(x_test)
    # print results
    # print clf.score(x_test,y_test)
    return (results, y_test)


def getAccuracy(results, y_test):
    # Calculate accuracy
    correct = 0
    count = 0
    for item in results:
        if str(item) == str(y_test[count]):
            correct += 1
        count += 1
    print "Accuracy = " + str((float(correct) / float(len(y_test))) * 100) + "%"


# Calculate precision - from all positive, how many were predicted as positive?

# Calculate recall - from all positive predictions, how many were correct?

# Calculate F1 score


if __name__ == "__main__":
    main()
