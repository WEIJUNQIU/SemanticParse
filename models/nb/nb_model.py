#!/usr/bin/python
# -*- coding: utf-8 -*-
import os,sys
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '/../../utils/')
import logging
from numpy import *
from sklearn.ensemble import AdaBoostClassifier
from sklearn.svm import SVC
import numpy as np
from sklearn.naive_bayes import MultinomialNB
logger = logging.getLogger(os.path.splitext(__file__)[0])

class nb_model():
    def train(self, X, Y):
        self.model = MultinomialNB(alpha=1.0, fit_prior=True, class_prior=None)
        self.model.fit(X, Y)

    def predict(self, X):
        return self.model.predict(X)

    def predict_pro(self, X):
        return self.model.predict_proba(X)

    def get_score(self, X, Y):
        return self.model.score(X, Y)

    def get_feature_names(self):
        return self.model.classes_

    def load(self):
        return

    def dump(self):
        return

if __name__ == "__main__":
    sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '/../tfidf/')
    from tfidf_model import *
    data = ['这是 一个 测试 项目 标题','测试 标题', '项目 标题']
    tfidf = tfidf_model()
    Y = [1, 2, 3]
    X = np.array([[1,2,3], [2,3,4], [3,4,5]])
    # X = tfidf.train(data, Y)

    model = nb_model()
    model.train(X, Y)

    #print X
    print model.predict(X)
    print model.predict_pro(X)
    #print model.get_feature_names()
