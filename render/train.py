import sys, os
reload(sys)
sys.setdefaultencoding( "utf-8" )
import re, math, time
from PyQt4.QtGui import *
from PyQt4 import QtCore, QtGui, QtWebKit
import pickle

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '/../util/')
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '/../models/svm/')
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '/../models/adaboost/')
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '/../models/nb/')
from adaboost import *
from nb_model import *
import csv

class train_model():

    def __init__(self):
        self.xrange = [(0, 0), (1, 10), (10, 20), (20, 40), (40, 70), (70, 120), (120, 150), (150, 200),(200, 300),
            (300, 500), (500, 800), (800, 1500), (1500, 100000)]
        self.yrange = [(0, 10), (10, 50), (50, 150), (150, 300), (300, 500), (500, 800), (800, 1200), (1200, 2000),
                       (2000, 5000), (5000, 8000), (8000, 12000), (12000, 100000)]
        self.wordrange = [(0, 0), (0, 5), (5, 15), (15, 25), (25, 40), (40, 65), (65, 95),
            (95, 125), (125, 160), (160, 200), (200, 245), (245, 300), (300, 350), (250, 400), (400, 100000)]
        self.imgrange = [(0, 0), (0, 5), (5, 10), (10, 15), (15, 20), (20, 25), (25, 30),
            (30, 40), (40, 50), (50, 60), (60, 70), (70, 75), (75, 80), (80, 90), (90, 120), (120, 150), (150, 100000)]
        self.herfrange = [(0, 0), (0, 5), (5, 10), (10, 15), (15, 20), (20, 25), (25, 30),
            (30, 40), (40, 50), (50, 60), (60, 70), (70, 75), (75, 80), (80, 90), (90, 120), (120, 150), (150, 100000)]

    def sparse_x(self, x):
        for i, j in enumerate(self.xrange):
            if x in range(j[0], j[1]+1):
                return i

    def sparse_y(self, y):
        for i, j in enumerate(self.yrange):
            if y in range(j[0], j[1]+1):
                return i

    def sparse_img(self, num):
        for i, j in enumerate(self.imgrange):
            if num in range(j[0], j[1]+1):
                return i

    def sparse_herf(self, num):
        for i, j in enumerate(self.wordrange):
            if num in range(j[0], j[1]+1):
                return i

    def sparse_word(self, num):
        for i, j in enumerate(self.wordrange):
            if num in range(j[0], j[1]+1):
                return i


if __name__=='__main__':
    model = train_model()
    ss = 0
    for ran in range(1,11):
        train_input = []
        train_label = []
        test_input = []
        test_label = []
        count = 0
        csvfile = file('/Users/qiuweijun/Desktop/semanticparse/data/crum_total.csv', 'rb')
        reader = csv.reader(csvfile)
        for i in reader:
            tmp = []
            sw = model.sparse_x(int(i[5].replace(',', '')))
            sh = model.sparse_y(int(i[6].replace(',', '')))
            # print count, int(i[5].replace(',', '')), int(i[6].replace(',', ''))
            sw = float(sw)
            sh = float(sh)
            # print count, int(i[1].replace(',', '')), int(i[3].replace(',', ''))
            tmp.extend([model.sparse_x(int(i[1].replace(',', ''))), model.sparse_x(int(i[3].replace(',', ''))),
                        model.sparse_x(int(i[1].replace(',', '')))/sw, model.sparse_x(int(i[3].replace(',', '')))/sw])
            tmp.extend([model.sparse_y(int(i[2].replace(',', ''))), model.sparse_y(int(i[4].replace(',', ''))),
                        model.sparse_y(int(i[2].replace(',', '')))/sh, model.sparse_y(int(i[4].replace(',', '')))/sh])
            tmp.extend([model.sparse_y(int(i[7].replace(',', ''))), model.sparse_y(int(i[8].replace(',', ''))),
                        model.sparse_y(int(i[9].replace(',', '')))])
            # tmp.extend([int(i[1].replace(',', '')), int(i[2].replace(',', '')), int(i[3].replace(',', '')),
            #             int(i[4].replace(',', '')), int(i[1].replace(',', ''))/int(i[5].replace(',', '')),
            #             int(i[3].replace(',', ''))/int(i[5].replace(',', '')),
            #             int(i[2].replace(',', ''))/int(i[6].replace(',', '')),
            #             int(i[4].replace(',', ''))/int(i[6].replace(',', '')),
            #             int(i[7]),  int(i[8]), int(i[9])])
            if count in range((ran-1)*8000/10, ran*8000/10):
                test_input.append(tmp)
                test_label.append(int(i[0]))
            else:
                train_input.append(tmp)
                train_label.append(int(i[0]))
            count+=1

        print ran, len(train_input), len(train_label)
        tmodel = nb_model()
        tmodel.train(np.array(train_input), np.array(train_label))
        sss = tmodel.get_score(np.array(test_input), np.array(test_label))
        print sss
        ss+=sss


    print ss/10
    # with open('crum.pickle', 'wb') as fp:
    #     pickle.dump(model, fp)
    # print 'done'
