#!/usr/bin/python
# -*- coding: utf-8 -*-
import os,sys
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '/../../utils/')
import logging
from numpy import *
from sklearn.svm import OneClassSVM
import numpy as np
logger = logging.getLogger(os.path.splitext(__file__)[0])

class svm_model():
    def train(self, X, ker):
        self.model = OneClassSVM(kernel=ker, shrinking=True,random_state=1)
        self.model.fit(X)

    def predict(self, X):
        return self.model.predict(X)

if __name__ == "__main__":
    sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '/../tfidf/')
    from tfidf_model import *
    data = ['这是 一个 测试 项目 标题','测试 标题', '项目 标题']
    tfidf = tfidf_model()
    Y = [1, 2, 3]
    X = np.array([[1,2,3], [2,3,4], [3,4,5], [3,2,4], [5,3,2], [456,2,4], [2,4,5]])
    # X = tfidf.train(data, Y)

    model = svm_model()
    model.train(X, 'linear')

    #print X
    print model.predict(X)
    #print model.get_feature_names()
