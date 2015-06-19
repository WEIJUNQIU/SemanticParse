#!/usr/bin/python
# -*- coding: utf-8 -*-
import os,sys
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '/../../utils/')
from config import *
from sklearn.feature_selection import SelectKBest, chi2
from sklearn.feature_extraction.text import TfidfVectorizer
import cPickle as pickle
import logging
logger = logging.getLogger(os.path.splitext(__file__)[0])

class tfidf_model():
    def train(self, X, Y):
        #X为文本矩阵
        #Y为事先的分类结果
        self.vectorizer = TfidfVectorizer()
        tfidf = self.vectorizer.fit_transform(X)
        self.selector = SelectKBest(chi2, k = 'all')
        return self.selector.fit_transform(tfidf, Y)

    def transform(self, X):
        tfidf = self.vectorizer.transform(X)
        return self.selector.transform(tfidf)

    def get_feature_names(self):
        return self.vectorizer.get_feature_names()

    def load(self):
        with open(config().get('train', 'tfidf_result_path'), 'rb') as fp:
            model = pickle.load(fp)
        logger.info("read " + self.__class__.__name__ + " train result")
        self.vectorizer = model.vectorizer
        self.selector = model.selector

    def dump(self):
        with open(config().get('train', 'tfidf_result_path'), 'wb') as fp:
            pickle.dump(self, fp)
        logger.info("write " + self.__class__.__name__ + " train result")

if __name__ == "__main__":
    data = ['这是 一个 测试 项目 标题','测试 标题']
    trainer = tfidf_model()
    print trainer.train(data, [1,2])
    trainer.dump()
    print
    model = tfidf_model()
    model.load()
    print model.transform([data[1]]).toarray()
