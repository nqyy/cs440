# TextClassifier.py
# ---------------
# Licensing Information:  You are free to use or extend this projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to the University of Illinois at Urbana-Champaign
#
# Created by Dhruv Agarwal (dhruva2@illinois.edu) on 02/21/2019

import math
import re

"""
You should only modify code within this file -- the unrevised staff files will be used for all other
files and classes when code is run, so be careful to not modify anything else.
"""
class TextClassifier(object):
    def __init__(self):
        """Implementation of Naive Bayes for multiclass classification

        :param lambda_mixture - (Extra Credit) This param controls the proportion of contribution of Bigram
        and Unigram model in the mixture model. Hard Code the value you find to be most suitable for your model
        """
        self.messages = {}
        self.log_prior = {}
        self.word_count = {}
        self.v = set()
        self.class_word_count={}
        self.lambda_mixture = 0.0

    def count_words(self,words):
        w_c = {}
        for word in words:
            if word not in w_c:
                w_c[word] = 0.0
            w_c[word] += 1.0
        return w_c

    def fit(self, train_set, train_label):
        """
        :param train_set - List of list of words corresponding with each text
            example: suppose I had two emails 'i like pie' and 'i like cake' in my training set
            Then train_set := [['i','like','pie'], ['i','like','cake']]

        :param train_labels - List of labels corresponding with train_set
            example: Suppose I had two texts, first one was class 0 and second one was class 1.
            Then train_labels := [0,1]
        """        
        set_len = len(train_set)
        for label in train_label:
            if label not in self.messages:
                self.messages[label] = 0.0
            self.messages[label] += 1.0

        for key in self.messages.keys():
            self.log_prior[key] = math.log(self.messages[key]/set_len)
            self.word_count[key] = {}
            self.class_word_count[key] = 0.0
        
        zip_text_label = zip(train_set,train_label)
        labels = list(self.messages.keys())
        for text,label in zip_text_label:
            count = self.count_words(text)
            for x,y in count.items():
                if x not in self.v:
                    self.v.add(x)
                if x not in self.word_count[label]:
                    self.word_count[label][x] = 0.0
                    
                self.word_count[label][x] += y
                self.class_word_count[label] += y
                

        # TODO: Write your code here
        

    def predict(self, x_set, dev_label,lambda_mix=0.0):
        """
        :param dev_set: List of list of words corresponding with each text in dev set that we are testing on
              It follows the same format as train_set
        :param dev_label : List of class labels corresponding to each text
        :param lambda_mix : Will be supplied the value you hard code for self.lambda_mixture if you attempt extra credit

        :return:
                accuracy(float): average accuracy value for dev dataset
                result (list) : predicted class for each text
        """
        
        accuracy = 0.0
        result = []
        accurate_labels = 0
        labels = list(self.messages.keys())
        label_count = len(labels)
        for x,y in zip(x_set,dev_label):
            class_score = [0] * label_count
            count = self.count_words(x)
            for word,wc in count.items():
                if word not in self.v:
                    continue
                for i in range(label_count):
                    cur_label = labels[i]
                    total_words = self.class_word_count[cur_label]
                    log_i_temp = math.log((self.word_count[cur_label].get(word,0.0)+1)/(total_words+ len(self.v)))
                    class_score[i] += log_i_temp
            
            for i in range(label_count):
                class_score[i] += self.log_prior[labels[i]]
            
            class_index = class_score.index(max(class_score))
            pre_label = labels[class_index]
            #print(class_score," and predicted label is ",pre_label," and the correct label is ",y)
            
            if pre_label == y:
                accurate_labels +=1.0

            result.append(pre_label)
        accuracy = accurate_labels / len(x_set)    
        # TODO: Write your code here

        return accuracy,result

