import sys, os
reload(sys)
sys.setdefaultencoding( "utf-8" )
from sklearn import preprocessing
import re, math, time, random
from PyQt4.QtGui import *
from PyQt4 import QtCore, QtGui, QtWebKit
import pickle

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '/../util/')
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '/../models/svm/')
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '/../models/adaboost/')
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '/../models/nb/')
from adaboost import *
from svm_model import *
from nb_model import *
from sklearn.neighbors import NearestNeighbors
import csv

class train_model():

    def __init__(self):
        self.xrange = [(-10, 0), (1, 10), (10, 20), (20, 40), (40, 70), (70, 120), (120, 150), (150, 200),(200, 300),
            (300, 500), (500, 800), (800, 1500), (1500, 100000)]
        self.yrange = [(-10, 10), (10, 50), (50, 150), (150, 300), (300, 500), (500, 800), (800, 1200), (1200, 2000),
                       (2000, 5000), (5000, 8000), (8000, 12000), (12000, 100000)]
        self.wordrange = [(0, 0), (0, 5), (5, 15), (15, 25), (25, 40), (40, 65), (65, 95),
            (95, 125), (125, 160), (160, 200), (200, 245), (245, 300), (300, 350), (250, 400), (400, 100000)]
        self.imgrange = [(0, 0), (0, 5), (5, 10), (10, 15), (15, 20), (20, 25), (25, 30),
            (30, 40), (40, 50), (50, 60), (60, 70), (70, 75), (75, 80), (80, 90), (90, 120), (120, 150), (150, 100000)]
        self.herfrange = [(0, 0), (0, 5), (5, 10), (10, 15), (15, 20), (20, 25), (25, 30),
            (30, 40), (40, 50), (50, 60), (60, 70), (70, 75), (75, 80), (80, 90), (90, 120), (120, 150), (150, 100000)]
        self.arearange = [(0, 0), (0, 1), (1, 15), (15, 30), (30, 50), (50, 100), (100, 200), (200, 300), (300, 500),
                          (500, 800), (800, 1200), (1200, 1500), (1500, 2000), (2000, 4000), (4000, 10000)]

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

    def sparse_area(self, num):
        for i, j in enumerate(self.arearange):
            if num in range(j[0], j[1]+1):
                return i

    def get_features(self, line_data):
        tmp = []
        sarea = (round(float(line_data[9].replace(',', '')))/100)*(round(float(line_data[10].replace(',', '')))/100)
        t_area = (round(float(line_data[4].replace(',', '')))/100)*(round(float(line_data[5].replace(',', '')))/100)
        ratio = round(t_area/sarea, 5)
        if ratio > 1:
            return False
        sw = self.sparse_x(round(float(line_data[9].replace(',', ''))))
        sh = self.sparse_y(round(float(line_data[10].replace(',', ''))))
        sword = round(float(line_data[11].replace(',', '')))
        sherf = round(float(line_data[12].replace(',', '')))
        simg = round(float(line_data[13].replace(',', '')))

        # print t_area, sarea, t_area/sarea
        tmp.extend([self.sparse_x(float(line_data[2].replace(',', ''))),
                    self.sparse_x(float(line_data[4].replace(',', ''))),
                    self.sparse_x(float(line_data[2].replace(',', '')))/sw,
                    self.sparse_x(float(line_data[4].replace(',', '')))/sw])
        tmp.extend([self.sparse_y(float(line_data[3].replace(',', ''))),
                    self.sparse_y(float(line_data[5].replace(',', ''))),
                    self.sparse_y(float(line_data[3].replace(',', '')))/sh,
                    self.sparse_y(float(line_data[5].replace(',', '')))/sh])
        tmp.extend([self.sparse_area(round(t_area)), ratio])
        # tmp.extend([float(i[6].replace(',', '')), float(i[7].replace(',', '')),
        #             float(i[8].replace(',', ''))])
        tmp.extend([float(line_data[6].replace(',', '')), float(line_data[7].replace(',', '')),
                    float(line_data[8].replace(',', '')), float(line_data[6].replace(',', ''))/sherf,
                    float(line_data[6].replace(',', ''))/simg, float(line_data[6].replace(',', ''))/sword])

        return tmp

    def over_sampling(self, n_model, l_features, tmp_i, pre, next):
        nn = n_model.kneighbors(tmp_i, return_distance=False)
        _samples = []
        tmp_i = np.array([int(float(k)) for k in tmp_i])
        for i in xrange(0, 5):
            nn_index = nn[0][random.randint(2,5)]
            l_features[nn_index] = np.array([int(float(k)) for k in l_features[nn_index]])
            dif = l_features[nn_index] - tmp_i
            gap = np.random.random()
            a_tmp = tmp_i + gap * dif[:]
            a_tmp = pre+[str(int(m)) for m in a_tmp.tolist()]+next
            _samples.append(a_tmp)
        return _samples

        # dif = l_features[nn_index] - T[i]
        # t_index = tmp_l.index(current_l)
        # for i in t_index:
        #     instance = tmp_i[i]
        #     self.knn(tmp_i[i], tmp_i, )
        # pass


if __name__=='__main__':
    csvfile = file('/Users/qiuweijun/Desktop/semanticparse/data/616/crum_label.csv', 'rb')
    reader = csv.reader(csvfile)
    label_features = []
    for i in reader:
        label_features.append(i[2:9])
    #Learn nearest neighbours
    neigh = NearestNeighbors(n_neighbors = 5)
    neigh.fit(label_features)

    model = train_model()
    ss = 0
    #6591, 11554, 11817
    total_num = 6591
    fold_num = 5
    current_label = 1
    for ran in range(1,fold_num+1):
        train_input = []
        train_label = []
        test_input = []
        test_label = []
        flag = 0
        count = 0
        csvfile = file('/Users/qiuweijun/Desktop/semanticparse/data/616/crum.csv', 'rb')
        reader = csv.reader(csvfile)
        for i in reader:
            if int(i[0]) != -1:
                tmp_d = model.get_features(i)
                if tmp_d and count not in range((ran-1)*total_num/fold_num, ran*total_num/fold_num):
                    train_input.append(tmp_d)
                    if int(i[0]) == current_label:
                        train_label.append(int(i[0]))
                        gen_samples = model.over_sampling(neigh, label_features, i[2:9], i[0:2], i[9:14])
                        for new in gen_samples:
                            tmp_d = model.get_features(new)
                            if tmp_d:
                                train_input.append(tmp_d)
                                train_label.append(current_label)
                    else:
                        train_label.append(0)
            count += 1

        print ran, len(train_input), len(train_label)
        # tmodel = nb_model()
        # train_input = np.array(train_input)
        # scaler = preprocessing.StandardScaler().fit(train_input)
        # train_input_scaled = scaler.transform(train_input)

        tmodel = svm_model()
        tmodel.train( np.array(train_input), np.array(train_label), 'rbf')

        count = 0
        csvfile = file('/Users/qiuweijun/Desktop/semanticparse/data/616/crum.csv', 'rb')
        reader = csv.reader(csvfile)
        flat = 0
        sss = 0
        total = 0
        for i in reader:
            if int(i[0]) != -1:
                tmp_d = model.get_features(i)
                if tmp_d and count in range((ran-1)*total_num/fold_num, ran*total_num/fold_num):
                    test_input.append(tmp_d)
                    test_label.append(int(i[0]))
                    flat = 1
            elif flat == 1:
                # test_input_scaled = scaler.transform(np.array(test_input))
                prob = tmodel.predict_pro(np.array(test_input))
                total += 1
                tem = 0
                lab = -1
                for index, pro in enumerate(prob):
                    if tem < pro[1]:
                        tem = pro[1]
                        lab = test_label[index]
                if lab == current_label:
                    sss += 1
                test_input = []
                test_label = []
                flat = 0
            count += 1

        per = sss/float(total)
        print total, sss, per
        ss += per

    print ss/fold_num
