#!/usr/bin/python
# -*- coding: utf-8 -*-
import os,sys
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '/../../utils/')
from config import *
from sklearn.linear_model import SGDClassifier
import cPickle as pickle
import logging
from numpy import *
logger = logging.getLogger(os.path.splitext(__file__)[0])

class sgd_model():
    def train(self, X, Y):
        self.model = SGDClassifier(loss='log', penalty='elasticnet', alpha=5e-07, class_weight='auto', shuffle=True, n_jobs=-1, n_iter=60, l1_ratio=0.7)
        self.model.fit(X, Y)

    def predict(self, X):
        return self.model.predict(X)

    def predict_pro(self, X):
        return self.model.predict_proba(X)

    def get_feature_names(self):
        return self.model.classes_

if __name__ == "__main__":
    sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '/../tfidf/')
    from tfidf_model import *
    data = ['这是 一个 测试 项目 标题','测试 标题']
    tfidf = tfidf_model()
    Y = [1, 2]
    X = tfidf.train(data, Y)

    model = sgd_model()
    model.train(X, Y)
    print model
    print model.predict(X)
    print model.get_feature_names()
