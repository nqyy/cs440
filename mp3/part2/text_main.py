# text_main.py
# ---------------
# Licensing Information:  You are free to use or extend this projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to the University of Illinois at Urbana-Champaign
#
# Created by Dhruv Agarwal (dhruva2@illinois.edu) on 02/21/2019

import csv
from TextClassifier import TextClassifier
import string

"""
This file contains the main application that is run for this part of the MP.
No need to modify this file
"""

def read_stop_words(filename):
    """
       Reads in the stop words which are used for data preprocessing
       Returns a set of stop words
    """
    stop_words=set()
    with open(filename) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')

        for row in csv_reader:
            for word in row:
                stop_words.add(word.strip(" '"))
    stop_words.remove('')

    return stop_words

def readFile(filename,stop_words):
    """
    Loads the files in the folder and returns a list of lists of words from
    the text in each file and the corresponding labels
    """
    translator = str.maketrans("", "", string.punctuation)
    with open(filename) as csv_file:
        labels = []
        data = []
        csv_reader = csv.reader(csv_file, delimiter=',')

        for row in csv_reader:
            labels.append(int(row[0]))
            row[2] = row[2].lower()
            text= row[2].translate(translator).split()
            text = [w for w in text if w not in stop_words]
            data.append(text)

    return data,labels


def load_dataset(data_dir=''):
    """

    :param data_dir: directory path to your data
    :return: both the train and test data sets
    """
    stop_words=read_stop_words(data_dir+'stop_words.csv')
    x_train, y_train = readFile(data_dir+'train_text.csv',stop_words)
    x_test, y_test = readFile(data_dir+'dev_text.csv',stop_words)

    return x_train,y_train,x_test,y_test

def compute_results(actual_labels,pred_labels):
    """

    :param actual_labels: Gold labels for the given texts
    :param pred_labels: Predicted Labels for the given texts
    """
    precision=[]
    recall = []
    for c in range(1,15):
        actual_c = {i for i in range(len(actual_labels)) if actual_labels[i] == c}
        pred_c = {i for i in range(len(pred_labels)) if pred_labels[i] == c}
        tp = len(actual_c.intersection(pred_c))

        if len(pred_c) > 0:
            precision.append(tp/len(pred_c))
        else:
            precision.append(0.0)

        recall.append(tp/len(actual_c))

    f1=[2 * (p * r) / (p+r) if (p+r) !=0.0 else 0.0 for p, r in zip(precision,recall) ]

    print ("Precision for all classes :",precision)
    print ("Recall for all classes:",recall)
    print ("F1 Score for all classes:",f1)

if __name__ == '__main__':
    x_train, y_train, x_test, y_test = load_dataset()
    MNB = TextClassifier()
    MNB.fit(x_train, y_train)

    accuracy,pred = MNB.predict(x_test, y_test)
    compute_results(y_test,pred)

    print("Accuracy {0:.4f}".format(accuracy))