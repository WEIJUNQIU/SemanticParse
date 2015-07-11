#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys, os
reload(sys)
sys.setdefaultencoding( "utf-8" )
import re

class test():

    def word2features(self, sent, i):
        word = sent[i][0]
        features = [
            'word.lower=' + word.lower(),
            'word[-3:]=' + word[-3:],
            'word[-2:]=' + word[-2:],
            'word.isupper=%s' % word.isupper(),
            'word.istitle=%s' % word.istitle(),
            'word.isdigit=%s' % word.isdigit(),
        ]
        if i > 0:
            word1 = sent[i-1][0]
            features.extend([
                '-1:word.lower=' + word1.lower(),
                '-1:word.istitle=%s' % word1.istitle(),
                '-1:word.isupper=%s' % word1.isupper(),
            ])
        else:
            features.append('BOS')

        if i < len(sent)-1:
            word1 = sent[i+1][0]
            features.extend([
                '+1:word.lower=' + word1.lower(),
                '+1:word.istitle=%s' % word1.istitle(),
                '+1:word.isupper=%s' % word1.isupper(),
            ])
        else:
            features.append('EOS')

        return features


    def sent2features(self, sent):
        return [self.word2features(sent, i) for i in range(len(sent))]

    def sent2labels(self, sent):
        return [label for token, label in sent]

    def sent2tokens(sent):
        return [token for token, label in sent]



if __name__ == "__main__":
    count = 0
    f = open("/Users/qiuweijun/Desktop/study/nlp/实体词/dataset_617173/train_words.txt", "rb")
    train_data = []
    while True:
        line = f.readline()
        if line:
            content = []
            sentences = re.split('。/nt|，/nt|；/nt|：/nt', line)
            for sen in sentences:
                words = sen.split(' ')
                content.extend([(w.split('/')) for w in words if len(w)>0])
            train_data.extend([content])
        else:
            break
    f.close()

    T = test()
    X_train = [T.sent2features(s) for s in train_data]
    y_train = [T.sent2labels(s) for s in train_data]